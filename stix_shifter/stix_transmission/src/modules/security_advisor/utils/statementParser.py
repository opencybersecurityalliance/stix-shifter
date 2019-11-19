class StatementParser:

    def cleaner(self, entity):

        if entity.find("[") == 0  and  entity.find("]") == len(entity)-1:
            return entity[1:len(entity)-1].strip()

        if entity.find("[") == 0 :
            return entity[1:].strip()

        if entity.find("]") == len(entity) -1 :
            return entity[:len(entity)-1].strip()
        else:
            return entity.strip()

    def evaluate_or(self, splitted, list):

        for elem in splitted:
            not_split = elem.split("NOT")
            if( len(not_split) == 1 ):
                sub = not_split[0].strip()
                sub = not_split[0].split("=")
                key = sub[0].strip()
                value = sub[1].strip()
                list.append( (key, value) )

            else :
                for i in range(len(not_split)):

                    sub = not_split[i].strip()
                    sub = not_split[i].split("=")   
                    key = sub[0].strip()
                    value = sub[1].strip()
                    if i == 0:
                        list.append( (key , value) )
                    if i == 1:
                        list.append( (key + "~not~", value))

        return list

    def slpit_and_eval_or(self, splitted):
        
        splitted  = splitted.split("AND")
        list_OR  = []
        for i in range(0, len(splitted)):       
            cleaned_entity  =  self.cleaner(splitted[i])

            split_OR = cleaned_entity.split("AND")
            self.evaluate_or(split_OR, list_OR )

        return list_OR

    def parser(self, statement):

        list_AND = []
        split_AND = statement.split("OR")

        for i in split_AND:
            list_AND.append(self.slpit_and_eval_or(i))

        return list_AND

        