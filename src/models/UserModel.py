import random

from neo4jrestclient import client

from classes import User, Word, WordView, WordListView
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

                q = """
                    MATCH (u:User{email:"%s"})-[r]-(w:Word{name:"%s"})
                    CREATE (u)-[newR:%s{correct:%d, incorrect:%d}]->(w)
                    delete r
                    return newR.correct, newR.incorrect
                """ % (user.email, word.name, label, result_correct, result_incorrect)

                print(acc)
                new_seen = self._db.query(q)
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

    def get_forgotten_words(self, user: User) -> list:
        try:
            query = """
                MATCH (u:User{email:"%s"})-[:Forgotten]->(forgottenWords:Word)
                RETURN forgottenWords LIMIT %d
            """ % (user.email, self.word_set * 4)
            results = self._db.query(query)
            return WordModel.parse_words(results)
        except Exception as e:
            print(e)
            return []

    def get_recommended_words(self, user: User) -> list:
        try:
            query = """
                MATCH (u:User{email:"%s"})-[:Seen]->(w)<-[:Seen]-(colleges:User),
                      (colleges)-[:Seen]->(recW:Word)
                WHERE NOT (u)-[:Seen]->(recW) AND NOT (w)-[:Learnt]->(recW) AND NOT (w)-[:Forgotten]->(recW)
                RETURN recW LIMIT %d
            """ % (user.email, self.word_set * 4)
            results = self._db.query(query)
            return WordModel.parse_words(results)
        except Exception as e:
            print(e)
            return []

    def get_recommended_model_list(self, user=None) -> list:
        try:
            recommended_words = list()
            if user:
                recommended_words = self.get_forgotten_words(user) + self.get_recommended_words(user)
            if len(recommended_words) < self.word_set * 4:
                recommended_words = recommended_words + self.get_random_recommendation()

            recommended_words = recommended_words[:self.word_set * 4]

            return self.shuffle_recommendation_model(recommended_words)
        except Exception as e:
            print(e)
            return []

    def get_random_recommendation(self) -> list:
        try:
            query = """
                MATCH (w:Word)
                WHERE rand() < 0.5
                return w limit %d
            """ % (self.word_set * 4)
            results = self._db.query(query)
            return WordModel.parse_words(results)
        except Exception as e:
            print(e)
            return []

    def shuffle_recommendation_model(self, recommended_words) -> list:
        random_list_words = random.sample(range(0, len(recommended_words)), len(recommended_words))[:self.word_set]

        recommended_model = list()
        for i in random_list_words:
            definitions = []
            for j in random.sample(range(0, 4), 4):
                if j == 2:
                    definitions.append(recommended_words[i].definition)
                else:
                    definitions.append(recommended_words[random.randint(0, len(recommended_words) - 1)].definition)
            model = WordView(recommended_words[i], definitions)
            recommended_model.append(model)
        return recommended_model

    def get_accuracy(self, correctness, incorrectness):
        return correctness / (correctness + incorrectness + self._accuracy_rate)

    def get_label(self, percents):
        if percents >= 0.70:
            return self._learnt
        elif percents <= 0.40:
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

    def get_word_list_view(self, user: User) -> WordListView:
        # query = """
        #     optional match (u:User{email:"%s"})-[:Seen]->(wSeen:Word)
        #     optional match (u)-[:Forgotten]->(wForgotten:Word)
        #     optional match (u)-[:Learnt]->(wLearnt:Word)
        #     return wSeen, wForgotten, wLearnt
        # """ % user.email
        query = """
            match (u:User{email:"%s"})-[:Seen]->(wSeen:Word)
            return wSeen
        """ % user.email
        results = self._db.query(query)
        seen_list = WordModel.parse_words(results)

        query = """
            match (u:User{email:"%s"})-[:Forgotten]->(wForgotten:Word)
            return wForgotten
        """ % user.email
        results = self._db.query(query)
        forgotten_list = WordModel.parse_words(results)

        query = """
            match (u:User{email:"%s"})-[:Learnt]->(wLearnt:Word)
            return wLearnt
        """ % user.email
        results = self._db.query(query)
        learnt_list = WordModel.parse_words(results)

        # for element in results.elements:
        #     seen_list.append(element[0])
        #     forgotten_list.append(element[1])
        #     learnt_list.append(element[2])

        return WordListView(seen_list, learnt_list, forgotten_list)
