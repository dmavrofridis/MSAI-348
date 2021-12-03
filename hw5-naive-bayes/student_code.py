import math
import re

movie_stars = 0
movie_id = 1
movie_review = 2
special_characters_to_replace_list = [",", ".", ":", ";", "?", "-", "!", "(", ")", "*", "$", "%", "&", "(", ")", "*",
                                      "+", "/", "<", "=", ">", "@", "[", "]", "^", "_", "`", "{", "'", "~", "}",
                                      "r'\r'", "\n",
                                      r"\\", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
characters_to_replace_list = ["to ", "the ", "a ", "in ", "as ", "of ", "on ", "he ", "this ",
                              "its ", "for ", "him ", "make ", "there ", "it ", "these ",
                              "he ", "she ", "his ", "it's ", "is", "are ", "me ", "an ",
                              "i ", "and ", "that ", "with "]


class Bayes_Classifier:

    def __init__(self):
        self.positive_review_dict = {}
        self.negative_review_dict = {}
        self.positive_review_word_count = 0
        self.negative_review_word_count = 0
        self.total_reviews = 0
        self.positive_reviews = 0
        self.negative_reviews = 0
        self.sum_of_positive_review_frequencies = 0
        self.sum_of_negative_review_frequencies = 0

    def train(self, lines):
        # First step before training is to load the data appropriately, clean them and store them
        movies = self.load_data(lines)
        # Call the movie analyzer to return the number of positive reviews, negative reviews and the dictionaries
        # which contain the words for each positive and negative reviews accompanied by their frequency
        self.positive_reviews, self.positive_review_dict, self.negative_reviews, self.negative_review_dict = self.review_analyzer(
            movies)
        # assign the total reviews found
        self.total_reviews = len(lines)
        # get the count of total words collected for positive and negative reviews
        self.positive_review_word_count = len(self.positive_review_dict)
        self.negative_review_word_count = len(self.negative_review_dict)
        # sum the frequencies of all words for positive and negative reviews
        self.sum_of_positive_review_frequencies = sum(self.positive_review_dict.values())
        self.sum_of_negative_review_frequencies = sum(self.negative_review_dict.values())

        print(self.positive_review_word_count)
        print(self.negative_review_word_count)

    def classify(self, lines):
        predictions = []
        # load the classification (test) data
        movies = self.load_data(lines)

        for movie in movies:

            positive_probability = math.log(self.positive_reviews / self.total_reviews)
            negative_probability = math.log(self.negative_reviews / self.total_reviews)

            for word in movie[movie_review:]:
                if word in self.positive_review_dict.keys():
                    positive_probability = positive_probability + math.log((self.positive_review_dict[word] + 1) / (
                            self.positive_review_word_count + self.sum_of_positive_review_frequencies))
                else:
                    positive_probability = positive_probability + math.log(1 / (
                            self.positive_review_word_count + self.sum_of_positive_review_frequencies + self.sum_of_negative_review_frequencies))

                if word in self.negative_review_dict.keys():
                    negative_probability = negative_probability + math.log((self.negative_review_dict[word] + 1) / (
                            self.negative_review_word_count + self.sum_of_negative_review_frequencies))
                else:
                    negative_probability = negative_probability + math.log(1 / (
                            self.negative_review_word_count + self.sum_of_negative_review_frequencies + self.sum_of_positive_review_frequencies))

            if positive_probability >= negative_probability:
                predictions.append("5")
            else:
                predictions.append("1")

        return predictions

    def load_data(self, lines):
        data_set = []
        # First step, we have to split the lines into columns by | in order to get the id, stars ands review
        for row in lines:
            split_row = row.split('|')
            data_set.append(split_row)

        for movie in data_set:
            # assign the id and stars of the movie and cast them as integers
            '''movie[movie_id] = int(movie[movie_id])
            movie[movie_stars] = int(movie[movie_stars])'''
            # finally access the movie review text and format it by removing unnecessary characters
            movie[movie_review] = self.clean_movie_review(movie[movie_review])
            movie[movie_review:] = movie[movie_review].split(' ')
        return data_set

    def clean_movie_review(self, text_review):
        # Remove any uneccesary chracters in the review text
        # make the text lowercase so it is easier to work with
        text_review = text_review.lower()
        for character in special_characters_to_replace_list:
            text_review = text_review.replace(character, " ")
        for character in characters_to_replace_list:
            text_review = text_review.replace(character, " ")
        return text_review

    def review_analyzer(self, movie_data):
        negative_reviews = 0
        positive_reviews = 0
        negative_review_dict = {}
        positive_review_dict = {}
        for movie in movie_data:
            is_positive_review = False
            if movie[movie_stars] == "5":
                # it was a positive review
                positive_reviews += 1
                is_positive_review = True
            else:
                # it was a negative review
                negative_reviews += 1

            for word in movie[movie_review:]:
                # check each word of the moview review and assign it a value if it doesnt exist,
                # if found again increment it by 1
                if is_positive_review:
                    if word in positive_review_dict.keys():
                        positive_review_dict[word] = positive_review_dict[word] + 1
                    else:
                        # does not exist yet, word seen first time
                        positive_review_dict[word] = 1
                else:
                    if word in negative_review_dict.keys():
                        negative_review_dict[word] = negative_review_dict[word] + 1
                    else:
                        # does not exist yet, word seen first time
                        negative_review_dict[word] = 1

        return positive_reviews, positive_review_dict, negative_reviews, negative_review_dict
