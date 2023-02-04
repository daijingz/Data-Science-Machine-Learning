import pandas as pd

dataset0 = {'Release Year': [], 'Title': [], 'Origin/Ethnicity': [], 'Director': [],
            'Cast': [], 'Genre': [], 'Wiki Page': [], 'Plot': []}


def FileIO(address: str):
    df = pd.read_csv(address)
    for i in df['Release Year']:
        dataset0['Release Year'] += [i]

    for i in df['Title']:
        dataset0['Title'] += [i]

    for i in df['Origin/Ethnicity']:
        dataset0['Origin/Ethnicity'] += [i]

    Dir = []
    for i in df['Director']:
        if ', ' in i:
            realName = i.split(', ')
        elif ' and ' in i:
            realName = i.split(' and ')
        else:
            realName = []
        if len(realName) > 0:
            Dir += [str(realName)]
        else:
            Dir += [i]
    dataset0['Director'] = Dir

    for i in df['Cast']:
        dataset0['Cast'] += [i]

    for i in df['Genre']:
        dataset0['Genre'] += [i]

    for i in df['Wiki Page']:
        dataset0['Wiki Page'] += [i]

    for i in df['Plot']:
        dataset0['Plot'] += [i]


def Overall(address: str):
    df = pd.read_csv(address)
    print("Total Movies: " + str(len(df)))

    earliest, latest = 1930, 2000
    for i in dataframe0['Release Year']:
        if int(i) > latest:
            latest = i
        elif int(i) < earliest:
            earliest = i
    print("Start from Year " + str(earliest) + ". Ends at Year " + str(latest) + ".")

    maxLen, minLen = 0, 50
    maxWords, minWords = 0, 100
    for i in dataframe0['Title']:
        if len(i) > maxLen:
            maxLen = len(i)
        elif len(i) < minLen:
            minLen = len(i)

        if len(i.split(" ")) > maxWords:
            maxWords = len(i.split(" "))
        elif len(i.split(" ")) < minWords:
            minWords = len(i.split(" "))
    print()
    print("Title Maximum Letters: " + str(maxLen))
    print("Title Minimum Letters: " + str(minLen))
    print()
    print("Title Maximum Words: " + str(maxWords))
    print("Title Minimum Words: " + str(minWords))
    print()

    origins = []
    for i in dataframe0['Origin/Ethnicity']:
        if origins.count(i) == 0 and i != 'Unknown':
            origins += [i]
    print("Movie Origin: " + str(origins))


Directors = []


def findDirectors(Dir: list):
    for i in dataset0['Director']:
        temp = []
        if ' and ' in i:
            temp = i.split(' and ')
        elif ', ' in i:
            temp = i.split(', ')
        else:
            temp += [i]

        if len(temp) > 0:
            for j in temp:
                if Dir.count(j) == 0 and j != 'Unknown':
                    Dir += [j.replace('[', '').replace(']', '').replace('\'', '')]


FileIO('C:\\Users\\david\\Downloads\\archive\\wiki_movie_plots_deduped.csv')
dataframe0 = pd.DataFrame(data=dataset0)
# print(dataframe0)

Overall('C:\\Users\\david\\Downloads\\archive\\wiki_movie_plots_deduped.csv')
findDirectors(Directors)
print(str(Directors))
print(len(Directors))
