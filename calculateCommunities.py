import os


"""
QUALITY FUNCTIONS:

1: Newman-Girvan Modularity quality function
2: 

"""



COMUNIDADES_MAXIMAS = 15


os.system("./gen-louvain/convert -i out_graph -o graph.bin")
os.system("./gen-louvain/louvain graph.bin -l -1 -v > graph.tree")

# nivel -l 3       CAMBIAR SI SALE ERROR :'v
os.system("./gen-louvain/hierarchy graph.tree -l 3 > graph_node2comm_level3")

dict_communities = {}
dict_user = {}

with open('graph_node2comm_level3', 'r') as file:
	for row in file:
		user, community = row.split()
		if(community in dict_communities):
			dict_communities[community].append(user)
		else:
			dict_communities[community] = [user]
		dict_user[user] = community

dict_final = {}

itera = 0

for k in sorted(dict_communities, key=lambda k:len(dict_communities[k]), reverse=True):
	if(itera == COMUNIDADES_MAXIMAS):
		break
	print k + '  ' + str(len(dict_communities[k]))
	dict_final[k] = dict_communities[k]
	itera +=1
	
print "Comunidades reconocidas: " + str(len(dict_final))




out_final = open("userCommunities","w")

with open('out_graph_users','r') as file:
	for row in file:
		userId, user = row.split()
		community = 0
		if(dict_user[user] in dict_final):
			community = dict_user[user]
			out_final.write(str(userId) + ' ' + str(user) + ' ' + str(community) + '\n')

out_final.close()


#print dict_communities
