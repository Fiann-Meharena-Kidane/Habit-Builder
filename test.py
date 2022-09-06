import requests

response=requests.get('https://zenquotes.io/api/quotes')
data=response.json()

for entry in data:
    quote=entry['q']
    author=entry['a']
    print(quote, author)













# print(final_data)

# print(updated_data.split('|')[:-1])


# for i in updated_data.split('|')[:-1]:
#     if not i=='':
#         print(int(i))
# result=['2', '2', '3', '4']

#
# list=['3','4','5']
#
# for x in range(len(list)):
#     list[x]=int(list[x])
#
# print(list)