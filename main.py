import csv
import numpy
import sys
import time



# Optimized? No! Functional? Yes!!
import re


class MarkovChain:
    START = "_START"
    END = "_END"

    def __init__(self, state_length=1):
        self.model = {}  # {state : list of {next word : count}}
        self.state_length = state_length
        self.state = []
        self.reset()

    def reset(self):
        self.state = [MarkovChain.START] * self.state_length

    """"Feed the chain with a segment of data, such as a complete sentence. This data should implicitly have a
    beginning and an end """

    def feed_text(self, text):
        data = text.split(' ')
        # We use _START and _END as our delimiters for beginning and and ending, respectively.
        # I don't think Donny has ever even used an underscore.
        data = ([MarkovChain.START] * self.state_length) + data
        data.append(MarkovChain.END)

        for i in range(len(data) - self.state_length):
            state = tuple(data[i:i + self.state_length])
            # print(state)
            next_state = data[i + self.state_length]
            # print(next_state)

            # print ("State {0} transitions to {1}".format(state, next_state))

            if state not in self.model:
                self.model[state] = {}
            if next_state not in self.model[state]:
                self.model[state][next_state] = 1
            else:
                self.model[state][next_state] += 1

    """Transistions to the next state, returning it."""
    def next(self):
        if self.has_ended():
            raise ValueError("This chain has already reached its end state! To walk through it again, use reset()")

        next_options = self.model[tuple(self.state)]
        next_values = numpy.array(list(next_options.values()))
        # print(next_options)
        # print(next_values)
        prob_normalized = next_values / sum(next_values)
        choice = numpy.random.choice(list(next_options.keys()), p=prob_normalized)
        self.state.append(choice)
        self.state.pop(0)
        return choice

    def has_ended(self):
        return MarkovChain.END in self.state

    def walk(self):
        result = []
        while not self.has_ended():
            result.append(self.next())
        result.pop()
        self.reset()
        return ' '.join(result)




def csv_import(database):
    with open('realDonaldTrump.csv.txt', encoding='utf-8') as f:
        reader = csv.reader(f)
        data = list(reader)
        i = 0
        for row in data:
            i += 1
            try:
                # lazy formatting/encoding error fix.
                # It works so I wont complain, though it would be better to fix the root problem. I know this is awful.
                tweet = row[2].replace('\n', " ").replace("  ", " ").replace('"', '').replace('&amp;', '&').replace('â€"', '—').replace('â€”', '–').replace("â€˜", '‘').replace("â€™", "’").replace("â€œ", "“").replace("â€", "”")
                database.feed_text(tweet)

            except UnicodeDecodeError as err:
                print("FAIL {0}".format(err.encoding, err.object))


def main():
    chain = MarkovChain(2)
    # csv_import(chain)
    # chain.feed_text("Tremendous things, tremendous people, tremendous country! We have the best country. Truly tremendous and the best people too. Wonderful!")
    # for m in chain.model:
        # print('State {0} transitions to {1}'.format(m, chain.model[m]))
    csv_import(chain)
    start_time = time.time()
    # print(time.time())
    for i in range(2000):
        result = re.split('(?<=[.!?]) +', chain.walk())
        result_trimmed = ""
        chars = 0
        for sentence in result:
            chars += len(sentence)
            if chars > 140:
                break
            result_trimmed += sentence + ' '
        if(len(result_trimmed)) > 0:
            print(result_trimmed)
    # print(time.time() - start_time)
    # print(time.time())
    csv_import(chain)


if __name__ == '__main__':
    main()


