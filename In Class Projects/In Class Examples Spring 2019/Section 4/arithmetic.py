
class Arithmetic():

    def __init__(self,  ):
#        self.initial_val = initial_val
        print("There are no initial values")
        
        
    def add_values(self, a, b):
        total = a + b
        return total
    
    def add_list(self, list_obj):
        total = 0
        for val in list_obj:
            total += val

        return total
    
    def vector_addition(self, list1, list2):
        vector_total_list = []
        n1 = len(list1)
        n2 = len(list2)
        if n1 == n2:
            for i in range(n1):
                vector_total_list.append(self.add_values(list1[i], list2[i]))
        return vector_total_list

arithmetic = Arithmetic()
print(arithmetic)
#print(arithmetic.__init__)
#print(arithmetic.initial_val)
#print(arithmetic.__dict__)
#
#list1 = [3,5,7,9]
#list2 = [4,2,6,4]
#print(arithmetic.add_values(1,2))
#print(arithmetic.add_list(list1))
#print(arithmetic.vector_addition(list1,list2))