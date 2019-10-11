import yaml


def ebay_yaml(dir_name):
    yamlDict = {
        'name': 'ebay_api_config',
        'api.ebay.com': {
            'compatability': 719,
            'appid': 'Ferdinan-resellso-PRD-cd8cefb65-140b4985',
            'certid': 'PRD-d8cefb659764-8fc5-49ce-a86f-9549',
            'devid': '2c5c79f0-9e4a-4f13-b222-3af6d04588f3',
            'token': 'AgAAAA**AQAAAA**aAAAAA**oSFAXQ**nY+sHZ2PrBmdj6wVnY+sEZ2PrA2dj6ANl4ShCpGGpg+dj6x9nY+seQ**dA8GAA**AAMAAA**p+9+4BcVdcfdUX4UsaQd3gm/vjCr0qtg5lOx2mOWkhlr2kLLvUMkK3Peog4ZDBlmEwbRqQ69qfdzahE9gmD6UWDzQEbRTEvZZQ4QJqjj1ejzWoinaPkT4tqbF5RI11OWyG9orBK7U17EijZSbYiHOaCmMZz0mkI74IIJGgN/QANeHafKiqpPE8me8RFaMK0LZ+4vsHxSVTMD4FJYU/ySjkRs2Es2vC7F6cKCLyrC2HMzUR3zgfqiDpomKco3J3NTswwGTf+c6tvIrc2q5YI8mXVEvsH/FUc17IEhCHBJkp76FEs5OKOdGvnkeELKBu210DsGykZfkmyHYrBrS5XOD3dFwTWIh1shi8Q22qNV0tjILvRpyjy755GjUw1lQDmOPwAkdAZsuWR0yNpIYzBtgGOmOef6mMAgriz77rDLxi7AdF2uuShKV0RDOMnq1huty2VMCpkcP4X5y1mlxuvMcktia2bTxigFLtylk5rifYlaWqJUep/JGK6Bz2xBOMPx9JgGfvlnYgw59HXFVc8o8t2jrkbqGXkohsRV0oUGWxE5fITO/mu5NqQ81Xt+1lJbU1TgWDiYao7WKgrUZzR+dDcLWf8gshr/ftZm/Fzf6wFgod/z9WAowW9emKe8wn8VqXA11OtpKVYkrvPQv5cNXphlo2T8AzHGC09j/0eNG9LWWiTo4G+m8nvh3nEuu15yUVWmFtddPY94c6xs3z4UZQkUOUBbnr8+1iOx5JI2l4X6/r7xW6wjzotoBusa+AHk'
        },
        'svcs.ebay.com': {
            'appid': 'Ferdinan-resellso-PRD-cd8cefb65-140b4985',
            'version': '1.0.0'
        }}

    with open(f"{dir_name}\\ebay.yaml", "w+") as yamlfile:
        yaml.dump(yamlDict, yamlfile, default_flow_style=False)
