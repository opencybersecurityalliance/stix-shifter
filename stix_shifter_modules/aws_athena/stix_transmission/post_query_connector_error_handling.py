    
from venv import logger
import regex as re
import time
from stix_shifter_modules.aws_athena.stix_transmission import status_connector

class PostQueryConnectorErrorHandler():
    async def check_status_for_missing_column(client, search_id, query):
        """Creates a status check loop to see if the query fails with a column doesn't exist exception. If it does, return the query with the offending column removed.
            If it does not, return with "CONNECTOR_FACTORY_SUCCESS"

        Args:
            client (RestApiClientAsync) 
            search_id (String): For each query sent to Athena, a job is created that runs in till it finishes. This ID is used to find the job and access it's results.
            query (String): The query that will be modified if a missing column error occurs.

        Returns:
            String: Returns either a modified query, or a special key that can be used to know that the query was successful and to stop.
        """        
        status = status_connector.StatusConnector(client)
        column_to_delete = ""
        
        #Wait ten seconds if the status is RUNNING. Exits early if the status is not RUNNING.
        for i in range(10):
            time.sleep(1)
            status_response = await status.create_status_connection(search_id)
            #Checks if there is a message that can be read and if that message matches the column not found message.
            if(status_response != None and "message" in  status_response):
                match = re.search(f"Column '(.*)' cannot be resolved", status_response["message"])
                if(match):
                    #If there is a match, return the column name.
                    column_to_delete = match.group(1)
                    break
            elif(status_response != None and "status" in status_response and status_response["status"] != "RUNNING"):
                #If there is no match and the status is not running, than stop trying and exit with the success message.
                break
                
        if(column_to_delete != ""):
            return PostQueryConnectorErrorHandler._remove_invalid_column_table(column_to_delete, query)
        else:
            #May not always be successful, just that no column error is occurring.
            return "CONNECTOR_FACTORY_SUCCESS"
       
    
    def _remove_invalid_column_table(column_to_remove, query):
        """ Uses regex to iterate over the query and replace all comparison operations using the invalid column

        Args:
            column_to_remove (string): This is the name of the column that should be removed from the query.
            query (String): This is the current query that is failing. It should contain a column that needs to be removed.

        Returns:
            String : Returns the modified query with the column comparisons replaced with either TRUE or FALSE.
        """        
        #These are the possible forms for a left expression in a comparison
        COLUMN_NAME_PATTERN="([\\w\\d]*(?:\\.[\\w\\d]+)*)"
        VARCHAR_CAST_LEFT_EXPRESSION = f"CAST\\({COLUMN_NAME_PATTERN} as varchar\\)"
        REAL_CAST_LEFT_EXPRESSION = f"CAST\\({COLUMN_NAME_PATTERN} as real\\)"
        LOWER_LEFT_EXPRESSION = f"lower\\({COLUMN_NAME_PATTERN}\\)"
        #These are the possible forms for a right expression in a comparison
        LOWER_RIGHT_EXPRESSION="lower\\(.*?\\)"
        BRACKET_RIGHT_EXPRESSION="\\(.*?\\)"
        QUOTE_RIGHT_EXPRESSION="\\\'.*?\\\'"
        
        #These are the possible forms for an operator
        OPERATORS=">|>=|<|<=|!=|LIKE|IN|="
        
        #The general format for the pattern is {left expression} {operator} {right expression}. In order to get the column name, it needs to match on the left expression. 
        standard_pattern = f"((?:{VARCHAR_CAST_LEFT_EXPRESSION}|{REAL_CAST_LEFT_EXPRESSION}|{LOWER_LEFT_EXPRESSION}|{COLUMN_NAME_PATTERN}) ({OPERATORS}) (?:{LOWER_RIGHT_EXPRESSION}|{BRACKET_RIGHT_EXPRESSION}|{QUOTE_RIGHT_EXPRESSION}))"
        #Match Expressions are unique. They act as a function, for example regexp(string, pattern). Standard pattern is like ID = 5 format.
        match_pattern = f"((REGEXP_LIKE)\\((?:{VARCHAR_CAST_LEFT_EXPRESSION}|{REAL_CAST_LEFT_EXPRESSION}|{LOWER_LEFT_EXPRESSION}|{COLUMN_NAME_PATTERN}|{QUOTE_RIGHT_EXPRESSION}), '.*?'\\))"
        
        logger.debug(f"The failing column name : {column_to_remove}")
        logger.debug(f"Current query : {query}")
        logger.debug(f"Attempt to match the standard comparison pattern : {standard_pattern}")
        
        #Matches against the standard pattern, this gets all of the comparison expressions in the query except for TRUE/FALSE.
        #It checks each comparison against the offending column and replaces any that match with TRUE or FALSE
        all_comparison_strings = re.findall(standard_pattern, query, flags=re.IGNORECASE)
        if (len(all_comparison_strings) > 0):
            for comparison in all_comparison_strings:
                filtered_comparison_list = [item for item in comparison if item != ""]
                if(column_to_remove in filtered_comparison_list[1]):
                    logger.debug(f"The following comparison expression will be replaced (standard): {filtered_comparison_list[0]}" )
                    
                    #If the column doesn't exist and the comparison is a != it will always be true.
                    #In the case of <,>,>=,<=, the number doesn't exist, thus it is false.
                    #In the case of =, it will never = the value, thus it must be false.
                    #In the case of IN or LIKE, the value will always resolve to FALSE because something, can't be in nothing.
                    #Match will always resolve to false. This one may be true if the match is impossible (that however is a weird edge case), thus false.
                    if("!=" in filtered_comparison_list[2]):
                        query = query.replace(comparison[0], f"TRUE")
                    else:
                        query = query.replace(comparison[0], f"FALSE")
        
        #Matches against the match pattern, this gets all of the comparison expressions in the query except for TRUE/FALSE.
        #It checks each comparison against the offending column and replaces any that match with TRUE or FALSE
        all_match_strings = re.findall(match_pattern, query, flags=re.IGNORECASE)
        if (len(all_match_strings) > 0):
            for comparison in all_match_strings:
                filtered_comparison_list = [item for item in comparison if item != ""]
                if(column_to_remove in filtered_comparison_list[2]):
                    logger.debug(f"The following comparison expression will be replaced (match) : {filtered_comparison_list[0]}" )

                    #If the column doesn't exist and the comparison is a != it will always be true.
                    #In the case of <,>,>=,<=, the number doesn't exist, thus it is false.
                    #In the case of =, it will never = the value, thus it must be false.
                    #In the case of IN or LIKE, the value will always resolve to FALSE because something, can't be in nothing.
                    #Match will always resolve to false. This one may be true if the match is impossible (that however is a weird edge case), thus false.
                    query = query.replace(comparison[0], f"FALSE")
        
        return query