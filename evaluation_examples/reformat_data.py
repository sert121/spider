import json





def reformat(training_data:str,table_metadata:str):
    """
    training_data: json file containing the training data
    table_metadata: json file containing the table metadata
    """
    counter = 0
    for item in training_data:
        counter += 1
        instruction = item['question']
        sql = item['query']
        table_id = item['db_id']
        for table in table_metadata:
            if table.get('db_id') == table_id:
                table_dict = table
        
        # list of table names
        table_names = table_dict['table_names']
        table_columns_types = list(zip(table_dict['column_names'],table_dict['column_types']))
        name_dict, schema_dict,table_str_reps = {},{},[]
        # schema dict is a list of dictionaries with each dictionary containing the table name and its columns
        name_dict = { i:table_names[i] for i in range(len(table_names))}

        for i in range(len(table_columns_types)):
            col_details, col_type = table_columns_types[i]
            name_index, col = col_details
            if name_index == -1:
                continue

            t_name = name_dict[name_index]



            if schema_dict.get(t_name) is None:
                schema_dict[t_name] = []
                schema_dict[t_name].append([col,col_type])
            else:
                schema_dict[t_name].append([col,col_type])
        
        for key,val in schema_dict.items():
            tabular_str = f""" -- Table: {key} 
columns : {val}
"""
            table_str_reps.append(tabular_str)
            
        tabular_str = "\n".join(table_str_reps)
        #zip the columns and types together

        prompt = f"""
        -- Language PostgreSQL
        -- Tables: 
            {tabular_str}

You are a SQL code translator. You have been given the Table data above. Your role is to translate natural language to PostgreSQL. 
You should not select columns that are not part of the tables provided to you. Think step by step.
Your only output should be SQL code. Do not include any other text. Only SQL code.

Translate `{instruction}` to a syntactically-correct PostgreSQL query.
        """
        print(prompt,'\n*****************\n')
        if counter >2:
            break
        counter+=1


def load_json_file(file_path):
    with open(file_path) as f:
        json_data = json.load(f)
    return json_data


if __name__ == '__main__':
    training_data = load_json_file('./examples/train_spider.json')
    table_metadata = load_json_file('./examples/tables.json')
    reformat(training_data, table_metadata)
