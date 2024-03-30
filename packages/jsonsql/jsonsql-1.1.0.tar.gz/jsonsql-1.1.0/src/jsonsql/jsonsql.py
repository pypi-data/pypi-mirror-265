class JsonSQL():
    def __init__(self, allowed_queries: list=[], allowed_items: list=[], allowed_tables: list=[], allowed_connections: list=[], allowed_columns: dict={}):
        """Initializes JsonSQL instance with allowed queries, items, tables, 
        connections, and columns.
        
        Args:
        allowed_queries (list): Allowed SQL query strings. 
        allowed_items (list): Allowed SQL SELECT fields.
        allowed_tables (list): Allowed SQL FROM tables.
        allowed_connections (list): Allowed SQL JOIN conditions.
        allowed_columns (dict): Allowed columns per table.
        """
        self.ALLOWED_QUERIES = allowed_queries
        self.ALLOWED_ITEMS = allowed_items
        self.ALLOWED_TABLES = allowed_tables
        self.ALLOWED_CONNECTIONS = allowed_connections
        self.ALLOWED_COLUMNS = allowed_columns

        self.LOGICAL = ("AND", "OR")
        self.COMPARISON = ("=", ">", "<", ">=", "<=", "<>","!=")
        self.SPECIAL_COMPARISON = ("BETWEEN", "IN")

    def is_another_column(self, value:str):
        return value in self.ALLOWED_COLUMNS

    def is_special_comparison(self, comparator:str, value, valuetype):
        """Checks if a comparator and value match the special comparison operators.
    
        Special comparison operators include BETWEEN and IN. This checks if the 
        comparator is one of those, and if the value matches the expected format.
        
        Args:
            comparator (str): The comparison operator.
            value: The comparison value.
            valuetype: The expected type of the comparison value.
        
        Returns:
            bool: True if it is a valid special comparison, False otherwise.
        """
        def all_values_allowed(value, valuetype):
            """Checks if all values in a list are of the specified type.
        
            Args:
                value (list): The list of values to check.
                valuetype: The expected type of each value.
            
            Returns:
                bool: True if all values match the expected type, False otherwise.
            """
            valid = True
            for entry in value:
                if not isinstance(entry, valuetype) and not self.is_another_column(entry):
                    valid = False
                    break
            return valid

        if (not isinstance(value, list) and not self.is_another_column(value)) or not all_values_allowed(value, valuetype):
            return False
        
        if comparator == "BETWEEN" and len(value) == 2:
            return True

        elif comparator == "IN" and len(value) > 0:
            return True
        
        return False

    def is_valid_comparison(self, column:str, comparison:dict):
        """Checks if a comparison operator and value are valid for a column.
        
        Validates that the comparator is a valid operator, and the value is the 
        expected type for the column or a valid special comparison.
        
        Args:
            column (str): The column name.
            comparison (dict): The comparison operator and value.
        
        Returns:
            bool: True if the comparison is valid, False otherwise.
        """
        comparator = list(comparison)[0]

        if comparator not in self.COMPARISON and comparator not in self.SPECIAL_COMPARISON:
            return False
        
        value = comparison[comparator]
        if (not isinstance(value, list) and self.is_another_column(value)) or isinstance(value, self.ALLOWED_COLUMNS[column]) or self.is_special_comparison(comparator, value, self.ALLOWED_COLUMNS[column]):
            return True
        return False

    def logic_parse(self, json_input: dict):
        if len(json_input) == 0:
            return False, "Nothing To Compute"
        
        value: str = list(json_input.keys())[0]
        
        if value not in self.ALLOWED_COLUMNS and value not in self.LOGICAL and value not in self.SPECIAL_COMPARISON and value not in self.COMPARISON:
            return False, f"Invalid Input - {value}"
        
        elif value in self.LOGICAL and not isinstance(json_input[value], list):
            return False, f"Bad {value}, non list"

        elif (value in self.ALLOWED_COLUMNS and not self.is_valid_comparison(value,json_input[value])):
            if isinstance(json_input[value],dict):
                value0 = list(json_input[value])[0]
                if value0 not in self.COMPARISON and value0 not in self.SPECIAL_COMPARISON:
                    return False, f"Non Valid comparitor - {value0}"
            return False, f"Bad {value}, non {self.ALLOWED_COLUMNS[value]}"

        if self.is_valid_comparison(value, json_input[value]):
            
            comparator = list(json_input[value])[0]
            if comparator in self.COMPARISON and not self.is_another_column(json_input[value][comparator]):
                return True, f"{value} {comparator if comparator != '!=' else '<>'} ?", json_input[value][comparator]
            
            elif comparator in self.COMPARISON and self.is_another_column(json_input[value][comparator]):
                return True, f"{value} {comparator if comparator != '!=' else '<>'} {json_input[value][comparator]}", ()
            
            elif comparator in self.SPECIAL_COMPARISON:
                if comparator == "BETWEEN":
                    return True, f"{value} BETWEEN ? AND ?", tuple(json_input[value][comparator])

                elif comparator == "IN":
                    return True, f"{value} IN ({'?' if len(json_input[value][comparator]) == 1 else ('?,'*len(json_input[value][comparator]))[:-1]})", tuple(json_input[value][comparator])

            return False, f"Comparitor Error - {comparator}"
        
        elif value in self.LOGICAL and isinstance(json_input[value], list):
            if len(json_input[value]) < 2:
                return False, "Invalid boolean length, must be >= 2"
            
            data = []
            safe = (True, "")
            for case in json_input[value]:
                evaluation = self.logic_parse(case)
                if not evaluation[0]:
                    safe = evaluation
                    break

                data.append(evaluation[1:])

            if not safe[0]:
                return safe

            params = []
            output = []
            for entry in data:
                if isinstance(entry[1],tuple):
                    for sub in entry[1]:
                        params.append(sub)
                else:
                    params.append(entry[1])
                output.append(entry[0])

            params = tuple(params)

            if not isinstance(params,tuple):
                params = (params,)

            data = f"({f" {value.upper()} ".join(output)})"

            return True, data, params
        
    def sql_parse(self, json_input: dict):
        required_inputs: dict = {"query":str, "items":list, "connection":str, "table":str}
        for item in required_inputs:
            if item not in json_input and item != "connection":
                return False, f"Missing argument {item}"
            elif not isinstance(json_input[item],required_inputs[item]):
                return False, f"{item} not right type, {required_inputs[item]}"
            
        if json_input["query"] not in self.ALLOWED_QUERIES:
            return False, f"Query not allowed - {json_input["query"]}"

        for item in range(len(json_input["items"])):
            if json_input["items"][item] not in self.ALLOWED_ITEMS:
                return False, f"Item not allowed - {json_input["items"][item]}"
                
        if json_input["table"] not in self.ALLOWED_TABLES:
            return False, f"Table not allowed - {json_input['table']}"
        
        if json_input["connection"] not in self.ALLOWED_CONNECTIONS:
            return False, f"Connection not allowed - {json_input['connection']}"
        
        sql_string = f"{json_input["query"]} {",".join(json_input["items"])} FROM {json_input["table"]}"

        if "logic" in json_input:
            logic_string = self.logic_parse(json_input["logic"])
            if not logic_string[0]:
                return False, f"Logic Fail - {logic_string[1]}"
            
            return True, f"{sql_string} {json_input["connection"]} {logic_string[1]}", logic_string[2]
        
        return sql_string