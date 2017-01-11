from neo4jrestclient import client

from classes import User, Word
from config import Graph
from models.WordModel import WordModel


class UserModel(Graph):
    word_set = 10

    _seen = "Seen"  # (50,80)%
    _learnt = "Learnt"  # [80,100]%
    _forgotten = "Forgotten"  # [0,50]%

    _recommendation = "Recommendation"
    _label = "User"

    _accuracy_rate = 0.1

    def create(self, user):
        user_node = self._db.nodes.create(email=user.email, password=user.password)
        user_node.labels.add(self._label)

    def update(self, user):
        person = self._db.labels.get(self._label).get(email=user.email)
        if person[0]:
            person[0].set('email', user.email)
            person[0].set('password', user.password)

    def get(self, user):
        try:
            person = self._db.labels.get(self._label).get(email=user.email)
            if person and person[0]:
                return User(person[0].properties['email'], person[0].properties['password'])
        except Exception as e:
            print(e)
        else:
            return None

    def get_node(self, user):
        try:
            person = self._db.labels.get(self._label).get(email=user.email)
            if person[0]:
                return person[0]
        except Exception as e:
            print(e)
        else:
            return None

    def is_valid(self, user):
        try:
            person = self._db.labels.get(self._label).get(email=user.email)
            if person[0]:
                return True
        except Exception as e:
            print(e)
        else:
            return False

    def seen_word(self, user, word, correct: bool):
        try:
            query = """
                MATCH (u:%s{email:"%s"})-[r]-(w:Word{name:"%s"}) return r.correct, r.incorrect
            """ % (self._label, user.email, word.name)
            results = list(self._db.query(query))

            correct_stat = 1 if correct else 0
            incorrect_stat = 1 if not correct else 0

            if results:
                result_correct = results[0][0] + correct_stat
                result_incorrect = results[0][1] + incorrect_stat
                acc = self.get_accuracy(result_correct, result_incorrect)
                label = self.get_label(acc)

                delete_query = """
                        MATCH (u:%s{email:"%s"})-[r]-(w:Word{name:"%s"})
                        DELETE r
                    """ % (self._label, user.email, word.name)
                ex = self._db.query(delete_query)
                print(ex)
                change_query = """
                        CREATE (u:%s{email:"%s"})-[new:%s{correct: %d, incorrect: %d}]->(w:Word{name:"%s"})
                        return new.correct, new.incorrect
                    """ % (self._label, user.email, label, result_correct, result_incorrect,word.name)

                # query = """
                #     MATCH (u:%s{email:"%s"})-[r:%s]-(w:Word{name:"%s"})
                #     SET r.correct=%d, r.incorrect=%d
                #     return r
                # """ % (self._label, user.email, self._seen, word.name, result_correct, result_incorrect)
                print(acc)
                new_seen = self._db.query(change_query)
                print(new_seen)
            else:
                user_node = self.get_node(user)
                word_node = WordModel().get_node(word)
                if correct:
                    user_node.relationships.create(self._seen, word_node, correct=correct_stat,
                                                   incorrect=incorrect_stat)
                else:
                    user_node.relationships.create(self._forgotten, word_node, correct=correct_stat,
                                                   incorrect=incorrect_stat)

        except Exception as e:
            print(e)

    def get_recommended_words(self):
        try:
            n = 4
            query = """
                MATCH (n)
                WHERE rand() < 0.01
                return n limit """ + str(n) + """
            """
            results = list(self._db.query(query, returns=client.Node))
            word_list = [self.node_to_class(word[0]) for word in results]
            random_list1 = random.sample(range(0, n), n)
            random_list2 = random.sample(range(0, n), n)

            for i in range(n):
                temp = word_list[random_list1[i]].definition
                word_list[random_list1[i]].definition = word_list[random_list2[i]].definition
                word_list[random_list2[i]].definition = temp
                if i != 0:
                    word_list[i].name = ""
            return word_list
        except Exception as e:
            print(e)
            return None

    def change_recommendation(self, user):
        try:
            query = """
                MATCH (u:User{email:"%s"})-[:Seen]->(w)<-[:Seen]-(colleges:User),
                      (colleges)-[:Seen]->(recW:Word),
                      (u)-[:Forgotten]->(forgottenWords:Word)
                WHERE NOT (u)-[:Seen]->(recW) AND NOT (w)-[:Learnt]->(recW) AND NOT (w)-[:Forgotten]->(recW)
                RETURN recW, forgottenWords LIMIT %d
            """ % (user.email, self.word_set)
            results = self._db.query(query)
            word_list = list()
            if results:
                for element in results.elements:
                    word_name = element[0]['data']['name']
                    word_definition = element[0]['data']['definition']
                    word_label = WordModel().get_label(element[0]['metadata']['labels'])

                    word_recW = Word(word_name, word_label, word_definition)

                    word_list.append(word_recW)


                    # query = """
                    #     MATCH (u:%s{email:"%s"})-[r:%s]-(w:Word)
                    #     return w, r.correct, r.incorrect
                    # """ % (self._label, user.email, self._seen)

                    # accuracy = list()
                    # results = Graph._db.query(query)
                    # avg_accuracy = 0
                    # for element in results.elements:
                    #     word = element[0]
                    #     correct = element[1]
                    #     incorrect = element[2]
                    #     if isinstance(correct, int) and isinstance(incorrect, int):
                    #         acc = self.get_accuracy(correct, incorrect)
                    #         avg_accuracy += acc
                    #         accuracy.append([word, acc])
                    # if len(accuracy) < self.word_set:
                    #     return
                    #     # for a in accuracy:
                    #     #     print(a[1])

        except Exception as e:
            print(e)

    def get_accuracy(self, correctness, incorrectness):
        return correctness / (correctness + incorrectness + self._accuracy_rate)

    def get_label(self, percents):
        if percents >= 0.80:
            return self._learnt
        elif percents <= 0.50:
            return self._forgotten
        return self._seen

    def get_all(self):
        try:
            user_list = list()
            users = self._db.labels.get(self._label).all()
            for user in users:
                user_list.append(User(user.properties['email'], user.properties['password']))
            return user_list
        except Exception as e:
            print(e)
            return None


if __name__ == '__main__':
    print("hello")
    user_model = UserModel()
    word_model = WordModel()
    Marko = User("markomihajlovicfm@gmail.com")
    Alter = Word("Alter", "", "")
    Abject = Word("Abject", "", "")
    Abdicate = Word("Abdicate", "", "")
    user_model.seen_word(Marko, Abject, True)
    # Pr = User("pr@gmail.com")
    # user_model.seen_word(Pr, Abdicate, True)
    # user_model.change_recommendation(Marko)

    # query = """
    #                 MATCH (u:User{email:"markomihajlovicfm@gmail.com"})-[r:Seen]-(w:Word)
    #                 return w, r.correct, r.incorrect
    #             """
    # accuracy = list()
    # results = Graph._db.query(query)
    # for element in results.elements:
    #     word = element[0]
    #     correct = element[1]
    #     incorrect = element[2]
    #     if isinstance(correct, int) and isinstance(incorrect, int):
    #         accuracy.append({'word': word, 'accuracy': correct/(correct+incorrect)})
    #     else:
    #         print(correct, incorrect)
    # for a in accuracy:
    #     print(a["accuracy"])
