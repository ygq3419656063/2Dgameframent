import pickle

class Person1:
    name="Mike"
    age=10
    @classmethod
    def updatename(cls,newname):
        cls.name=newname



with open("person1.pkl","wb") as file:
    pickle.dump(Person1,file)

# 反序列化对象从文件
#Person1.name="John"
Person1.updatename('John')

with open("person1.pkl", "rb") as file:
    loaded_person1 = pickle.load(file)
    #loaded_person1.name = "John"

print("读取的对象",loaded_person1.name,loaded_person1.age)
print("原始对象",Person1.name,Person1.age)