myAge = 0
while True :
	print ( myAge )
	if myAge >= 100 :
		OLD = True
		print ( OLD )
		break
	else :
		OLD = False
		print ( OLD )
	myAge = myAge + 1
print ( myAge )
print ( OLD )
