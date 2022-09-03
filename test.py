demo='3|6|5|4|'


dele='3'
updated_data=''
for value in demo:
    if not value==dele:
        updated_data+=value
    final_data=updated_data[1:]


print(final_data)

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