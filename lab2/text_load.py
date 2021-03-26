special_sign='$'
def load_text():
	with open("ustawa.txt") as file: 
   		data = file.read()	
   		data+='$'
   		return data
text1='bbbd'+special_sign  
text2='aabbabd'+special_sign
text3='ababcd'+special_sign
text4='abcbccd'+special_sign

