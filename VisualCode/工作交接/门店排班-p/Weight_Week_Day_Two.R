#  step4: edit renshu
max_person
max_person_edit
colSums(max_person_edit)

max_person_edit_boy
max_person_edit_girl

colSums(max_person_edit_boy)
# according fan wei judge
edit_boy <- as.matrix(copy(max_person_edit_boy))
edit_girl <- as.matrix(copy(max_person_edit_girl))



## 郑州------------
# edit_girl 
edit_boy[1,1]<- 7
edit_boy[1,2]<- 7
edit_boy[1,3]<- 7
edit_boy[1,4]<- 7
edit_boy[1,5]<- 7
edit_boy[1,6]<- 7
edit_boy[1,7]<- 7

edit_boy[2,6]<- 5
edit_boy[2,7]<- 5

edit_boy[2,1]<- 3
edit_boy[2,2]<- 3
edit_boy[2,3]<- 3
edit_boy[2,4]<- 3
edit_boy[2,5]<- 3
edit_boy[2,6]<- 3
edit_boy[2,7]<- 3

edit_boy[3,6]<- 7
edit_boy[3,7]<- 7

edit_girl[1,1]<- 7
edit_girl[1,2]<- 7
edit_girl[1,3]<- 7
edit_girl[1,4]<- 7
edit_girl[1,5]<- 7

edit_girl[2,1]<- 5
edit_girl[2,2]<- 5
edit_girl[2,3]<- 5
edit_girl[2,4]<- 5
edit_girl[2,5]<- 5

edit_girl[3,1]<- 9
edit_girl[3,2]<- 9
edit_girl[3,3]<- 9
edit_girl[3,4]<- 9
edit_girl[3,5]<- 9

edit_girl[1,6]<- 8
edit_girl[1,7]<- 8

edit_girl[2,6]<- 6
edit_girl[2,7]<- 6

edit_girl[3,6]<- 10
edit_girl[3,7]<- 10

edit_girl+edit_boy
write.csv(edit_girl+edit_boy,'clipboard')





# edit_dehua 

edit_boy[1,1]<- 7
edit_boy[1,2]<- 7
edit_boy[1,3]<- 7
edit_boy[1,4]<- 7
edit_boy[1,5]<- 7
edit_boy[1,6]<- 7
edit_boy[1,7]<- 7

edit_boy[2,1]<- 3
edit_boy[2,2]<- 3
edit_boy[2,3]<- 3
edit_boy[2,4]<- 3
edit_boy[2,5]<- 3
edit_boy[2,6]<- 5
edit_boy[2,7]<- 5

edit_boy[3,1]<- 7
edit_boy[3,2]<- 7
edit_boy[3,3]<- 7
edit_boy[3,4]<- 7
edit_boy[3,5]<- 7
edit_boy[3,6]<- 7
edit_boy[3,7]<- 7



edit_girl[1,1]<- 7
edit_girl[1,2]<- 7
edit_girl[1,3]<- 7
edit_girl[1,4]<- 7
edit_girl[1,5]<- 7

edit_girl[2,1]<- 5
edit_girl[2,2]<- 5
edit_girl[2,3]<- 5
edit_girl[2,4]<- 5
edit_girl[2,5]<- 5

edit_girl[3,1]<- 9
edit_girl[3,2]<- 9
edit_girl[3,3]<- 9
edit_girl[3,4]<- 9
edit_girl[3,5]<- 9

edit_girl[1,6]<- 8
edit_girl[1,7]<- 8

edit_girl[2,6]<- 6
edit_girl[2,7]<- 6

edit_girl[3,6]<- 10
edit_girl[3,7]<- 10

edit_girl+edit_boy
colSums(edit_girl+edit_boy)
write.csv(edit_girl+edit_boy,'clipboard')





## 南宁1店------------
# edit_girl 
edit_boy[1,1]<- 7
edit_boy[1,2]<- 7
edit_boy[1,3]<- 7
edit_boy[1,4]<- 7

edit_boy[2,1]<- 4
edit_boy[2,2]<- 4
edit_boy[2,3]<- 4
edit_boy[2,4]<- 4

edit_boy[3,1]<- 8
edit_boy[3,2]<- 8
edit_boy[3,3]<- 8
edit_boy[3,4]<- 8


edit_boy[1,5]<- 9
edit_boy[1,6]<- 9
edit_boy[1,7]<- 9
edit_boy[2,5]<- 4
edit_boy[2,6]<- 4
edit_boy[2,7]<- 4
edit_boy[3,5]<- 9
edit_boy[3,6]<- 9
edit_boy[3,7]<- 9



edit_girl[1,1]<- 7
edit_girl[1,2]<- 7
edit_girl[1,3]<- 7
edit_girl[1,4]<- 7

edit_girl[2,1]<- 5
edit_girl[2,2]<- 5
edit_girl[2,3]<- 5
edit_girl[2,4]<- 5

edit_girl[3,1]<- 9
edit_girl[3,2]<- 9
edit_girl[3,3]<- 9
edit_girl[3,4]<- 9


edit_girl[1,5]<- 8
edit_girl[1,6]<- 8
edit_girl[1,7]<- 8
edit_girl[2,5]<- 6
edit_girl[2,6]<- 6
edit_girl[2,7]<- 6
edit_girl[3,5]<- 10
edit_girl[3,6]<- 10
edit_girl[3,7]<- 10


person_da
colSums(edit_boy)
colSums(edit_girl)
write.csv(edit_girl+edit_boy,'clipboard')





# edit_dehua 


edit_girl+edit_boy
colSums(edit_girl+edit_boy)
write.csv(edit_girl+edit_boy,'clipboard')
