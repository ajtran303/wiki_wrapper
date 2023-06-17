import wikipedia

class NoSuggestionsError(Exception):
    pass

def parse_query(query):
    results = wikipedia.search(query, results=1)
    if len(results) == 0:
        query = wikipedia.suggest(query)
        if query == None:
            raise NoSuggestionsError
        else:
            return query
    else:
        print(results[0])
        return results[0]

def summarize(query):
    return wikipedia.summary(query, sentences=1)


if __name__ == '__main__':
    EXIT_CONDITIONS = {'q', 'quit', 'exit'}

    def _prompt_user():
        print('> Input topic to search:')
        text = input()

        if text in EXIT_CONDITIONS:
            _goodbye()
        else:
            print('    ', summarize(parse_query(text)))
            print()

    def _goodbye():
        print('Thanks and goodbye!')
        quit()

    print('Hint: type "quit" to exit!')
    print()

    while True:
        try:
            _prompt_user()
        except NoSuggestionsError:
            print('> Could not find anything about that. Try another topic!')
            continue
        except wikipedia.exceptions.PageError:
            print('> Could not find that topic! Try another topic!')
            continue
        except wikipedia.exceptions.DisambiguationError as d_err:
            suggestions = ['"' + suggestion + '"' for suggestion in d_err.options[:3]]
            print('> Could not find that topic! Do you mean:')
            print((' or ').join(suggestions) + '?')
            continue
        except EOFError:
            _goodbye()
        except KeyboardInterrupt:
            _goodbye()