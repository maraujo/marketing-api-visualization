import argparse
import pandas as pd
import itertools

NULL_VALUE = "NOTSELECTED"


class PandasDataset:
    expat_counter = 0
    @staticmethod
    def get_age_range(row):
        min_age = row["min_age"]
        max_age = row["max_age"]
        if max_age == NULL_VALUE and min_age == 18:
            return "{}+".format(int(min_age))
        if max_age == NULL_VALUE and min_age == 45:
            return "{}+".format(int(min_age))
        else:
            return "{}-{}".format(int(min_age), int(max_age))

    @staticmethod
    def get_pandas_dataset_from_file(filepointer):
        print "Reading data..."
        return pd.read_csv(filepointer.name)

    def get_expat_row(self, row_with_all, rows_with_locals):
        print "Get Expat Row: {}".format(self.expat_counter)
        self.expat_counter += 1
        expat_row = row_with_all.copy()
        expat_row["citizenship"] = "Expats"

        # same_necessary_columns = ["scholarity","interest","country_code","gender","language","min_age","max_age"]
        # for column in same_necessary_columns:
        #     rows_with_locals = rows_with_locals[rows_with_locals[column] == row_with_all[column]]
        # if len(rows_with_locals) != 1 and len(rows_with_locals) != 2:
        #     import ipdb;ipdb.set_trace()
        #     raise Exception("Should have 1 and only 1 local_row that matchs")
        # row_with_local = rows_with_locals.iloc[0]
        # expat_row["audience"] = row_with_all["audience"] - row_with_local["audience"]
        expat_row["audience"] = row_with_all["audience"]/2
        if expat_row["audience"] < 0:
            expat_row["audience"] = 0
        return expat_row


    def replace_specific_key_value(self, column, old_value, new_value):
        print "Replacing : {}:{} por {}:{}".format(column,old_value,column,new_value)
        self.data.loc[self.data[column] == old_value, column] = new_value
        print len(self.data)

    def insert_age_range_column(self):
        print "Inserting Age Range..."
        self.data["age_range"] = self.data.apply(lambda row: self.get_age_range(row), axis=1)
        print len(self.data)

    def check_not_permitted_empty_values(self):
        print "Checking Not Permitted Empty Values..."
        no_nan_columns = ["country_code", "gender", "audience"]
        for column in no_nan_columns:
            if self.data[column].isnull().values.any():
                raise Exception("Not Allowed Null at:" + column)
        print len(self.data)

    def replace_null_values(self):
        print "Replace Null Values..."
        self.data = self.data.fillna(NULL_VALUE)
        print len(self.data)

    def check_data_integrity(self):
        print "Checking Data Integrity..."
        list_of_categories = {
            "country_code": self.data["country_code"].unique(),
            "topic" : self.data["topic"].unique(),
            "age_range" : self.data["age_range"].unique(),
            "scholarity" : self.data["scholarity"].unique(),
            "language" : self.data["language"].unique(),
            "gender" : self.data["gender"].unique(),
            "citizenship": self.data["citizenship"].unique(),
            "is_denominator": self.data["is_denominator"].unique(),
        }
        error_counter = 0
        ok_counter = 0
        total = len(self.data[~self.data["is_denominator"]])
        for country_code in list_of_categories["country_code"]:
            for topic in list_of_categories["topic"]:
                for scholarity in list_of_categories["scholarity"]:
                    for language in list_of_categories["language"]:
                        for gender in list_of_categories["gender"]:
                            for citizenship in list_of_categories["citizenship"]:
                                for age_range in list_of_categories["age_range"]:
                                    instance = self.data[
                                        (country_code == self.data["country_code"]) &
                                        (topic == self.data["topic"]) &
                                        (scholarity == self.data["scholarity"]) &
                                        (language == self.data["language"]) &
                                        (gender == self.data["gender"]) &
                                        (age_range == self.data["age_range"]) &
                                        (False == self.data["is_denominator"]) &
                                        (citizenship == self.data["citizenship"])
                                    ]
                                    if topic == "demographic_data":
                                        continue
                                    if len(instance) != 1:
                                        if(len(instance) == 2) and instance.iloc[0]["experiment_id"] == instance.iloc[1]["experiment_id"]:
                                            continue
                                        import ipdb;ipdb.set_trace()
                                        error_counter += 1
                                        print "Error With topic:", country_code, topic, scholarity,language,gender,citizenship,age_range,error_counter, len(instance)
                                    else:
                                        ok_counter += 1
                                        print "{:.2f}%".format(ok_counter/float(total)*100)
        ok_counter = 0
        total = len(self.data[self.data["is_denominator"]])
        for country_code in list_of_categories["country_code"]:
            for scholarity in list_of_categories["scholarity"]:
                for language in list_of_categories["language"]:
                    for gender in list_of_categories["gender"]:
                        for citizenship in list_of_categories["citizenship"]:
                            for age_range in list_of_categories["age_range"]:
                                instance = self.data[
                                    (country_code == self.data["country_code"]) &
                                    (scholarity == self.data["scholarity"]) &
                                    (language == self.data["language"]) &
                                    (gender == self.data["gender"]) &
                                    (age_range == self.data["age_range"]) &
                                    (True == self.data["is_denominator"]) &
                                    (citizenship == self.data["citizenship"])
                                ]
                                if len(instance) != 1:
                                    error_counter += 1
                                    import ipdb;ipdb.set_trace()
                                    print "Error of denominator:", country_code, scholarity,language,gender,citizenship,age_range,error_counter, len(instance)
                                else:
                                    ok_counter += 1
                                    print "{:.2f}%".format(ok_counter / float(total) * 100)






    def delete_specific_key_value(self, key, value):
        print "Deleting specific key valye: {}:{}".format(key,value)
        self.data = self.data[self.data[key] != value]
        print len(self.data)

    def rename_column(self,old_name,new_name):
        print "Renaming: {}->{}".format(old_name, new_name)
        columns_names = {old_name : new_name}
        self.data = self.data.rename(columns=columns_names)
        print len(self.data)

    def insert_expats_native_rows(self):
        print "Adding Not Native Rows"
        rows_with_all = self.data[self.data["citizenship"] == NULL_VALUE]
        rows_with_locals = self.data[self.data["citizenship"] == "Locals"]
        rows_with_expats = rows_with_all.apply(lambda row_with_all: self.get_expat_row(row_with_all, rows_with_locals), axis=1)
        self.data = self.data.append(rows_with_expats)
        print len(self.data)

    def delete_column(self, column_name):
        print "Deleting Column:", column_name
        self.data = self.data.drop(column_name, 1)
        print len(self.data)

    def convert_language_to_language_group(self):
        print "Converting language to language group"
        self.replace_specific_key_value("language", "French (All)", "French")
        self.replace_specific_key_value("language","English (All)","English")
        self.replace_specific_key_value("language", "Spanish (All),Portuguese (All),Italian,German", "European")
        self.replace_specific_key_value("language", "Hindi,Urdu,Bengali,Tamil,Nepali,Punjabi,Telugu,Sinhala", "Indian")
        self.replace_specific_key_value("language", "Indonesian,Filipino,Malayalam,Thai", "SE Asia")
        print len(self.data)

    def delete_all_unnamed_columns(self):
        print "Delete all unnamed columns"
        for column in self.data.columns:
            if "Unnamed" in column:
                self.delete_column(column)

    def compress(self):
        pass
        # self.replace_specific_key_value("insterest","health", "H")
        # self.replace_specific_key_value("insterest", "luxury", "L")
        # self.replace_specific_key_value("citizenship", "Locals", "L")
        # self.replace_specific_key_value("citizenship", "Expats", "E")
        # self.replace_specific_key_value("gender", "Female", "F")
        # self.replace_specific_key_value("gender", "Male", "M")
        # self.replace_specific_key_value("age_range", "Male", "M")

        # self.rename_column("interest","i")
        # self.rename_column("country_code", "c")
        # self.rename_column("citizenship", "n")
        # self.rename_column("scholarity", "s")
        # self.rename_column("language", "l")

    def list_unique_topics(self):
        print "Unique Topics"
        print self.data["analysis_name"].unique()

    def generate_file_for_combination(self,combination):
        filtered_dataframe = self.data[(self.data["interest"] == combination[0]) | (self.data["interest"] == combination[1])]
        filtered_dataframe.to_csv("combinations/" + combination[0] + "-" + combination[1] + ".csv")

    def generate_combinations_files(self):
        print "Generating Combinations Files"
        interest_list = self.data["interest"].unique().tolist()
        for combination in itertools.combinations(interest_list,2):
            print combination[0],combination[1]
            self.generate_file_for_combination(combination)

    def process_data(self):
        self.replace_null_values()
        self.check_not_permitted_empty_values()

        self.rename_column("exclusion_behavior", "citizenship")
        self.rename_column("analysis_name", "topic")

        self.delete_specific_key_value("gender", 0)
        self.delete_specific_key_value("topic", "all health")
        self.delete_all_unnamed_columns()
        # self.delete_column("languages")

        self.convert_language_to_language_group()
        self.replace_specific_key_value("gender", 1, "Male")
        self.replace_specific_key_value("gender", 2, "Female")
        self.replace_specific_key_value("scholarity", "HIGH_SCHOOL,UNSPECIFIED,SOME_HIGH_SCHOOL", "ND")
        self.replace_specific_key_value("scholarity",
                                        "UNDERGRAD,HIGH_SCHOOL_GRAD,SOME_COLLEGE,ASSOCIATE_DEGREE,PROFESSIONAL_DEGREE",
                                        "HS")
        self.replace_specific_key_value("scholarity",
                                        "ALUM,IN_GRAD_SCHOOL,SOME_GRAD_SCHOOL,MASTER_DEGREE,DOCTORATE_DEGREE", "GRAD")
        self.replace_specific_key_value("citizenship", 6015559470580, "Locals")

        self.delete_specific_key_value("language", NULL_VALUE)
        self.delete_specific_key_value("country_code", "BH")
        self.delete_specific_key_value("language", "Arabic,English (All),Spanish (All),Portuguese (All),Italian,German,Hindi,Urdu,Bengali,Tamil,Nepali,Punjabi,Telugu,Sinhala,Indonesian,Filipino,Malayalam,Thai")
        self.delete_specific_key_value("scholarity", NULL_VALUE)

        self.insert_expats_native_rows()
        self.delete_specific_key_value("citizenship", "NOTSELECTED")
        # self.delete_specific_key_value("is_denominator", True)
        # self.delete_column("experiment_id")
        # self.delete_column("interest_id")
        # self.delete_column("interest")
        # self.delete_column("interest_query")
        # self.delete_column("placebo_id")
        # self.delete_column("placebo_query")
        # self.delete_column("ground_truth_column")
        self.insert_age_range_column()
        self.delete_specific_key_value("age_range", "18+")
        self.check_data_integrity()
        self.compress()
        self.generate_combinations_files()

    def save_file(self,filename):
        print "Saving file: {}".format(filename)
        self.data.to_csv(filename)

    def export_json(self, filter, filename):
        print "Saving json: {}".format(filename)
        json_dataset = pd.DataFrame()
        for key in filter:
            for value in filter[key]:
                json_dataset = json_dataset.append(self.data[self.data[key] == value])
        json_dataset.to_json(filename, orient="records")



    def __init__(self, filepointer):
        self.data = self.get_pandas_dataset_from_file(filepointer)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', help='JSON Query File')
    args = parser.parse_args()
    if args.input:
        filepointer = open(args.input, "r")
        pd_dataset = PandasDataset(filepointer)
        pd_dataset.process_data()
        pd_dataset.save_file("googlefusion.csv")
        filter = {"interest" : ["health","luxury"]}
        pd_dataset.export_json(filter,"data.json")
    else:
        raise Exception("No input data")
