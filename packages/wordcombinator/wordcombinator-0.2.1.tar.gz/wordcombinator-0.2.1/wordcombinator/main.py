from collections import defaultdict

def query_representation(queries,vocublaries):
    # Create a mapping of substrings to list the words that contains them.
    prefix_map = defaultdict(list)
    for word in vocublaries:
        for i in range(0,len(vocublaries)):
            prefix = word[:i]
            prefix_map[prefix].append(word)

    #Iterate over each query and generate all possible representations.
    result  = []
    for query in queries:
        representations = []
        generate_representations(query,0,"",prefix_map,representations)
        result.append(representations)

    return result

def generate_representations(query,index,current_rep,prefix_map,representations):
    # If we have reached the end of the query add the cuurent representations to the list.
    if index == len(query):
        representations.append(current_rep)
        return 

   # Get possible words that match all the possible substring.
    prefix = query[index:index+1]
    possible_words = prefix_map[prefix]

    #Iterate over each possible word.
    for word in possible_words:
        new_rep = current_rep + word + " "
        generate_representations(query, index+len(word),new_rep,prefix_map,representations)