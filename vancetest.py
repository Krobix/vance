import vance
#EXAMPLE

data = {
	"lol": 0,
	"lmao": "this is rad test",
	"cry": ";-;"
}

obj = vance.createVanceData(data=data)
with open("test.vance", "wb") as f:
	vance.dump(obj, f)
	

print(vance.load(open("test.vance", "rb")))
