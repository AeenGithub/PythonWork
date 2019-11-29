library(data.table)
library(tidyverse)
getwd()
# judge how assistant is usefual----
# shop_assistant[时>=9&时<=16,.N,]
# shop_id_nums <- shop_assistant[,.(sl=sum(净销数量,na.rm=TRUE)),导购员编码][sl>100,unlist(导购员编码),]
# week_day_sl <- shop_assistant[(导购员编码%in%shop_id_nums)&(节假日=='工作日'),.(sl=sum(净销数量,na.rm=TRUE)),.(星期)][order(星期)]
# week_day_hour_sl <-  shop_assistant[(导购员编码%in%shop_id_nums)&(节假日=='工作日'),.(sl=sum(净销数量,na.rm=TRUE)),.(星期,时)][order(星期,时)]
# 
# week_day_rs <- shop_assistant[(导购员编码%in%shop_id_nums)&(节假日=='工作日'),.(sl=sum(净销数量,na.rm=TRUE)),.(日期,星期,导购员编码)][,.(sl=sum(sl,na.rm=TRUE),.N),.(日期,星期)][,.(sl_mean = mean(sl,na.rm = TRUE),rs_mean = mean(N)),.(星期)][order(星期)]
# week_day_hour_rs <- shop_assistant[(导购员编码%in%shop_id_nums)&(节假日=='工作日'),.(sl=sum(净销数量,na.rm=TRUE)),.(日期,星期,时,导购员编码)][,.(sl=sum(sl,na.rm=TRUE),.N),.(日期,星期,时)][,.(sl_mean = mean(sl,na.rm = TRUE),rs_mean = mean(N),rs_max = max(N,na.rm = TRUE),rs_min = min(N,na.rm = TRUE)),.(星期,时)][order(星期,时)]
# week_day_hour_rs[,.(sl=mean(sl_mean,na.rm=TRUE),rs_max = mean(rs_max,na.rm=TRUE)),.(时)]
# week_day_hour_rs[,':='(ave_sl = sl_mean/rs_mean),]
# week_day_hour_rs[,.(ave_sl = mean(sl_mean,na.rm = TRUE),rs_mean=max(rs_mean,na.rm = TRUE)),.(时)][order(时)]
# 
# # zhou mo
# 
# week_day_rs <- shop_assistant[(导购员编码%in%shop_id_nums)&(节假日!='工作日')&(星期%in%c(6,7)),.(sl=sum(净销数量,na.rm=TRUE)),.(日期,星期,导购员编码)][,.(sl=sum(sl,na.rm=TRUE),.N),.(日期,星期)][,.(sl_mean = mean(sl,na.rm = TRUE),rs_mean = mean(N)),.(星期)][order(星期)]
# week_day_hour_rs <- shop_assistant[(导购员编码%in%shop_id_nums)&(节假日!='工作日')&(星期%in%c(6,7)),.(sl=sum(净销数量,na.rm=TRUE)),.(日期,星期,时,导购员编码)][,.(sl=sum(sl,na.rm=TRUE),.N),.(日期,星期,时)][,.(sl_mean = mean(sl,na.rm = TRUE),rs_mean = mean(N),rs_max = max(N,na.rm = TRUE),rs_min = min(N,na.rm = TRUE)),.(星期,时)][order(星期,时)]
# week_day_hour_rs[,.(sl=mean(sl_mean,na.rm=TRUE),rs_max = mean(rs_max,na.rm=TRUE)),.(时)]
# week_day_hour_rs[,':='(ave_sl = sl_mean/rs_mean),]
# week_day_hour_rs[,.(ave_sl = mean(sl_mean,na.rm = TRUE)),.(时)][order(时)]
# 
# 
# ggplot(week_day_hour_rs,aes(x=时,y=sl_mean,colour=factor(星期)))+geom_line()
# ggplot(week_day_hour_rs,aes(x=时,y=rs_mean,colour=factor(星期)))+geom_line()
# ggplot(week_day_hour_rs,aes(x=时,y=rs_max,colour=factor(星期)))+geom_line()
# ggplot(week_day_hour_rs,aes(x=时,y=rs_max,colour=factor(星期)))+geom_point()
# ggplot(week_day_hour_rs[时>=8&时<=24,,],aes(x=时,y=rs_mean))+geom_line()+facet_grid(星期~.)
# ggplot(week_day_hour_rs[时>=8&时<=24,,],aes(x=时,y=rs_max))+geom_line()+facet_grid(星期~.)
#step0: read_da base data-----
# shop_assistant <- 'H:\\360MoveData\\Users\\zhh\\Desktop\\190315-精细化排班\\python_1.csv' %>% fread(encoding = 'UTF-8')
# shop_assistant[,.N,门店名称]
# shop_assistant[,.N,导购员姓名]
# shop_assistant[,.N,导购员编码]

shop_da_left <- 'H:\\360MoveData\\Users\\zhh\\Desktop\\190315-精细化排班\\南宁.xlsx' %>% readxl::read_excel(sheet = '1RNN1S0101')
# shop_da_left <- 'H:\\360MoveData\\Users\\zhh\\Desktop\\190315-精细化排班\\南宁.xlsx' %>% readxl::read_excel(sheet = '1RNN1S0481') 
# pp_jiejiari <- 'H:\\360MoveData\\Users\\zhh\\Desktop\\190315-精细化排班\\节假日.xlsx' %>% readxl::read_excel(sheet=1) %>% as.data.table()
# pp_jiejiari[,.(日期,假日,班休),][,unique(假日),]
pp_jiejiari <- 'H:\\360MoveData\\Users\\zhh\\Desktop\\190315-精细化排班\\python2.xlsx' %>% readxl::read_excel(sheet=1) %>% as.data.table() %>% '['(,.(单据日期
,节假日,星期),)
sum(is.na(pp_jiejiari$节假日))

shop_da <- shop_da_left %>% left_join(pp_jiejiari,by=c('单据日期')) %>% as.data.table() %>% filter(!is.na(节假日))  %>% as.data.table()
# shop_da <- 'H:\\360MoveData\\Users\\zhh\\Desktop\\190315-精细化排班\\python_2.csv' %>% fread(encoding = 'UTF-8')
shop_da[,.N,门店名称]
str(shop_da)
# 门店销售时段分析

day_da <- 'H:\\360MoveData\\Users\\zhh\\Desktop\\190315-精细化排班\\python_3.csv' %>% fread()
str(day_da)

person_da <- 'H:\\360MoveData\\Users\\zhh\\Desktop\\190315-精细化排班\\南宁名单.xlsx' %>% readxl::read_excel(sheet='1RNN1S0101') %>% as.data.table() %>% '['(,.(营业员姓名,性别),)
# person_da <- 'H:\\360MoveData\\Users\\zhh\\Desktop\\190315-精细化排班\\百年德化一店导购人员名单.xlsx' %>% readxl::read_excel() %>% as.data.table()
# person_da <- 'H:\\360MoveData\\Users\\zhh\\Desktop\\190315-精细化排班\\粤海男女装人员名单.xlsx' %>% readxl::read_excel() %>% as.data.table()
max_person_sum <- nrow(person_da)
max_person_sum_boy <- nrow(person_da[性别=='男装',,])
max_person_sum_girl <- max_person_sum - max_person_sum_boy

shop_da[,.N,门店名称]

# step1: hour zhanbi of one day  hour:: zao zhong wan quan zhong   ----
shop_da[,.N,时][order(时)]
tem_shop_zhounei <- shop_da %>%'['(时>=8&时<=23&节假日=='工作日',.(节假日,时,总金额),) %>% '['(,.(jine = sum(总金额,na.rm=TRUE)),list(时)) %>% 
  '['(,':='(zhanbi = jine/sum(jine,na.rm=TRUE)),) %>% setorder(时)
tem_shop_zhoumo <- shop_da %>%'['(时>=8&时<=23&节假日=='周末',.(节假日,时,总金额),) %>% '['(,.(jine = sum(总金额,na.rm=TRUE)),list(时)) %>% 
  '['(,':='(zhanbi = jine/sum(jine,na.rm=TRUE)),) %>% setorder(时)

str(tem_shop_zhounei)
sum(tem_shop_zhounei$zhanbi)
ggplot(tem_shop_zhoumo,aes(x=时,y=zhanbi)) + geom_point()
ggplot(tem_shop_zhounei,aes(x=时,y=zhanbi)) + geom_point()

# write.csv(tem_shop_zhounei[时>=8&时<=23,,],'clipboard')
# write.csv(tem_shop_zhoumo[时>=8&时<=23,,],'clipboard')


get_max_time_quantum <- function(x,start_hour,end_hour){
  return (x[时>start_hour&时<end_hour,.(max_zhanbi = max(zhanbi)),])
}

get_max_time_quantum_sum <- function(x,start_hour,end_hour){
  return (x[时>start_hour&时<end_hour,.(max_zhanbi = sum(zhanbi)),])
}

# get_max_time_quantum_sum(tem_shop_zhoumo,8,10)

get_zhanbi_day <- function(wrapper_da = tem_shop_zhounei,wrapper_func = get_max_time_quantum ,start_hours =c(9,12,14),end_hours=c(18,21,24)){
  quantum_zhanbi <- purrr::pmap_df(list(x = start_hours,y= end_hours),function(x,y){return(wrapper_func(wrapper_da,x,y))})
  quantum_duan <- as.vector(quantum_zhanbi$max_zhanbi)
  # names(quantum_duan) <- c("zao", "zhong", "wan", "ye")
  return (quantum_duan)
}

get_zhanbi_day_zzw <- function(wrapper_da = tem_shop_zhounei ,start_hours =c(9-1,12-1,14-1,16-1,20-1),end_hours=c(12,14,16,20,24)){
  quantum_zhanbi <- purrr::pmap_df(list(x = start_hours,y= end_hours),function(x,y){return(get_max_time_quantum(wrapper_da,x,y))})
  quantum_duan <- as.vector(quantum_zhanbi$max_zhanbi)
  names(quantum_duan) <- c("z", "zz","zzw", "zw", "w")
  # names(quantum_duan) <-c('zao','zhong','wan')
  
  quantum_jiange_01 <- max(abs(quantum_duan[2]+quantum_duan[3] - quantum_zhanbi[1]),abs(quantum_zhanbi[2]+ quantum_zhanbi[3] - quantum_zhanbi[4]))
  quantum_jiange_02 <- max(abs(quantum_duan[4] + quantum_zhanbi[3] - quantum_duan[2]),abs(quantum_zhanbi[3] + quantum_zhanbi[4] - quantum_duan[5]))
  quantum_jiange_03 <- max(abs(quantum_jiange_01 - quantum_duan[2]),abs(quantum_jiange_02 - quantum_duan[4]))
  quantum_sum <- quantum_duan[1] + quantum_zhanbi[5] + quantum_jiange_01*2 + quantum_jiange_02*2 - quantum_jiange_03
  re_vector <- as.vector(unlist(c((quantum_duan[1]+quantum_jiange_01)/quantum_sum,
                                  (quantum_jiange_01+quantum_jiange_02-quantum_jiange_03)/quantum_sum,
                                  (quantum_duan[5]+quantum_jiange_02)/quantum_sum)))
  
  # quantum_jiange <- max(abs(quantum_duan[1] - quantum_zhanbi[2]),abs(quantum_zhanbi[3] - quantum_zhanbi[2]))
  # quantum_sum <- quantum_duan[1] + quantum_zhanbi[3] + quantum_jiange
  # re_vector <- as.vector(unlist(c(quantum_duan[1]/quantum_sum,quantum_jiange/quantum_sum,quantum_duan[3]/quantum_sum)))
  
  names(re_vector) <- c('zao','zhong','wan')
  return (re_vector)
}

get_zhanbi_day(tem_shop_zhounei,get_max_time_quantum,c(9,12,14),c(18,21,24))
get_zhanbi_day(tem_shop_zhounei,get_max_time_quantum_sum,c(9,12,14),c(18,21,24))
tem_shop_zhounei

zhounei_qz <-  get_zhanbi_day_zzw(wrapper_da = tem_shop_zhounei)
zhoumo_qz <- get_zhanbi_day_zzw(wrapper_da = tem_shop_zhoumo)

cbind(t(t(zhounei_qz)),t(t(zhounei_qz)),t(t(zhounei_qz)),t(t(zhounei_qz)),t(t(zhounei_qz)),t(t(zhoumo_qz)),t(t(zhoumo_qz)))

t(t(zhounei_qz))
t(t(zhoumo_qz))
# step2:get week weight  1-7 day quanzhong /renshu quan zhong----
tem_day_melt <- day_da %>%  '['(,.(jine = sum(当期零售金额,na.rm=TRUE)),list(年份周,星期))  %>% dcast.data.table(年份周~星期,value.var='jine') %>% 
  filter((年份周>=201601)&(年份周<=201653)) %>% as.data.table() %>% melt.data.table(id = 1, measure.vars = 2:8,variable.name = 'zhouji',value.name = 'jine') %>%
  as.data.table() %>% '['(,':='(mean_jine = mean(jine,na.rm = TRUE)),.(zhouji)) %>% '['(is.na(jine),':='(jine = mean_jine),)
tem_day <- tem_day_melt %>% dcast.data.table(年份周~zhouji,value.var='jine') %>% select(-年份周) %>%  colMeans() %>% t() %>% t() %>% as.data.table() %>% setnames('V1','lse')
rm(tem_day_melt)

tem_day %>% '['(,':='(quanzhong = lse/min(lse)),) # min quanzhong
tem_day %>% '['(,':='(quanzhong_ren = ceiling(nrow(person_da)*quanzhong/(max(quanzhong)))),)

#step3: get renshu of day day hour quan zhong----

as.matrix(tem_day$quanzhong_ren)%*%as.matrix(t(zhounei_qz))  # week： day*zzw
one_to_five <- as.matrix(zhounei_qz) %*% as.matrix(t(tem_day$quanzhong_ren))[1:5] # week: zzw*day
colnames(one_to_five) <- c('1','2','3','4','5')

as.matrix(tem_day$quanzhong_ren)%*%as.matrix(t(zhoumo_qz))  # week： day*zzw
sex_to_seven <- as.matrix(zhoumo_qz) %*% as.matrix(t(tem_day$quanzhong_ren))[6:7] # week: zzw*day
colnames(sex_to_seven) <- c('6','7')
max_person <- round(cbind(one_to_five,sex_to_seven))
colSums(max_person)

max_person_zb <- cbind(as.matrix(zhounei_qz)%*%matrix(1,1,5), as.matrix(zhoumo_qz)%*%matrix(1,1,2))
# person data  fen pei add to promise one person one day----

to_sleep_person_sum <- floor(max_person_sum/2)
max_people_day <- sum((max_person_sum-ceiling(colSums(max_person)))) - to_sleep_person_sum # need to add 
day_to_add_1_to5 <- floor(max_people_day*(tem_day[1:5,quanzhong]/sum(tem_day[1:5,quanzhong])))
day_to_add_1_to5_day <- round(t(t(zhounei_qz))%*%t(day_to_add_1_to5))
      
      
  day_to_add_1_to5_day[1,]  <- ceiling((day_to_add_1_to5)/2)
  day_to_add_1_to5_day[3,]  <- floor((day_to_add_1_to5)/2)
  day_to_add_1_to5_day[2,] <- 0
  
  day_to_add_1_to5_day[1,] <- day_to_add_1_to5_day[1,] +day_to_add_1_to5 - colSums(day_to_add_1_to5_day)
  
max_person_edit <- cbind(max_person[,1:5]+day_to_add_1_to5_day,max_person[,6:7]) # method1 to add

colSums(max_person)
colSums(max_person_edit)
person_da
(29-colSums(max_person_edit))
max_person_edit[1,6]<- 13
max_person_edit[1,7]<- 13
# person data  fen pei sex----
person_da[,.N,性别]
boy_sex_zb <- person_da[,.N,性别][性别=='男装',N,]/person_da[,.N,]
max_person_edit_boy <- round(max_person_edit*boy_sex_zb)
colSums(max_person_edit_boy)
max_person_edit_boy[3,5]  <- 7

max_person_edit_girl <- max_person_edit - round(max_person_edit*boy_sex_zb)
max_person_edit_girl[1,7] <- 4
max_person_edit_girl[1,6] <- 4

max_person_edit_girl+max_person_edit_boy
max_person_edit

round(max_person_edit_girl)
colSums(max_person_edit_girl)
max_person_sum_girl

round(max_person_edit_boy)
colSums(max_person_edit_boy)
max_person_sum_boy

max_person_edit_boy + max_person_edit_girl

# dehua
max_person_edit_girl[1,6] <- 4
max_person_edit_girl[1,7] <- 4

# yuehai

max_person_edit_girl[1,6] <- 4
max_person_edit_girl[1,7] <- 4

max_person_edit

max_person_sum_girl
sum(colSums(max_person_edit_girl) - max_person_sum_girl) 
max_person_sum_boy
colSums(max_person_edit_boy)
-(colSums(max_person_edit_boy) - max_person_sum_boy)

person_da[,.N,性别]

#step5:  person data fen pei mingzi zhounei ----

get_sex_paiban_zn <- function(changdu=max_person_sum_boy,max_zzw_sex = edit_boy,max_zhoutian = 25){
  zzwall <- as.data.table(matrix(NA,changdu,max_zhoutian))
  # zhouji <- 2

  for (zhouji in c(1:max_zhoutian)){
    print(zhouji)
    zhouji_real <- zhouji%% 5
    if(zhouji%%5==0){
      zhouji_real <- 5
    }
  zzw <- rep(c('早','中','晚'),max_zzw_sex[,(zhouji_real)])
  zzw_length <- length(zzw)
  tem_add_max <- rep(NA,changdu)
  
  # start_num <- if_else(zhouji==1,1,min(which(is.na(zzwall[[zhouji-1]]))))
  
  if(zhouji ==1){
    start_num <- 1
  }
  else if (zhouji>=2 ){
    if(sum(is.na(zzwall[[zhouji-1]]))>0){
      start_num <- min(which(is.na(zzwall[[zhouji-1]])))
    }else{
      start_num <- min(which(is.na(zzwall[[zhouji-2]])))
    }
    
  }


  
  if(start_num + zzw_length -1 <= changdu){
  tem_add_max[start_num:(start_num + zzw_length-1) ] <- zzw
  }
  else {
    tem_add_max[start_num:changdu ] <- zzw[1:(changdu-start_num+1)]
    tem_add_max[1:(zzw_length -(changdu -start_num +1)) ] <- zzw[(changdu-start_num+1+1):zzw_length]
  }
  
  zzwall[[zhouji]] <- tem_add_max
  }  
  return(zzwall)
}

get_sex_paiban_zn_new <- function(changdu=max_person_sum_boy,max_zzw_sex = edit_boy,max_zhoutian = 25){
  
}

tem_zhounei_girl <- get_sex_paiban_zn(changdu = max_person_sum_girl,max_zzw_sex = edit_girl,23)
tem_zhounei_boy <- get_sex_paiban_zn(changdu = max_person_sum_boy,max_zzw_sex = edit_boy,23)

get_paiban_xiuxi_week <- function(ori_da =tem_zhounei_boy ){
      ncol(ori_da)
      nrow(ori_da)
      tem_one <- ori_da[,1:5]
      
      sum(is.na(tem_one[,1:5]))
      colSums(is.na(tem_one))
      rowSums(is.na(tem_one))
      
      ori_da[,6:10]
      ori_da[,10:15]
      ori_da[,15:20]
}


get_sex_paiban_zm <-  function(changdu=max_person_sum_boy,max_zzw_sex = max_person_edit_boy,max_zhoutian = 25){
  zzwall <- as.data.table(matrix(NA,changdu,max_zhoutian))
  zzw_6 <- rep(c('早','中','晚'),max_zzw_sex[,(6)])
  zzw_7 <- rep(c('早','中','晚'),max_zzw_sex[,(7)])
  
  for(i in c(1:max_zhoutian)){
    print(i)
    if(i%%2==1){
      zzwall[,i] <- as.vector(zzw_6)
    }
    else{
      zzwall[[i]] <- as.vector(zzw_7)
    }
  }
  return(zzwall)
}


tem_zhoumo_girl <- get_sex_paiban_zm(changdu = max_person_sum_girl,max_zzw_sex = edit_girl,8)
tem_zhoumo_boy <- get_sex_paiban_zm(changdu = max_person_sum_boy,max_zzw_sex = edit_boy,8)
# bind boy and girl -----
tem_zhounei <- rbind(cbind(person_da[性别=='男装'],tem_zhounei_boy),cbind(person_da[性别=='女装'],tem_zhounei_girl))
colnames(tem_zhounei) <- c('姓名','性别',1:5,8:12,15:19,22:26,29:31)
# write.csv(tem_zhounei,'clipboard')

person_da
person_da[营业员姓名%in%c('李丽娟','丁明梅'),':='(性别='男装'),]
# deal zhoumo junheng----
sex_zm_jh <- function(zhoumo_paiban = tem_zhoumo_boy){
  re_tem_boy <- copy(zhoumo_paiban)
  zhoumo_da_base <- re_tem_boy[[1]]
  for (i in c(2:ncol(re_tem_boy))){
    next_index_num <- max(which(re_tem_boy[[i-1]] == '早'))
    fir_part <- lag(zhoumo_da_base,next_index_num)
    sec_part <- lead(zhoumo_da_base,length(zhoumo_da_base)-next_index_num)
    zhoumo_da <- c(sec_part[!is.na(sec_part)],fir_part[!is.na(fir_part)])
    re_tem_boy[[i]] <- zhoumo_da
  }
  return(re_tem_boy)
  }
tem_zhoumo <- rbind(sex_zm_jh(tem_zhoumo_boy),sex_zm_jh(tem_zhoumo_girl))
colnames(tem_zhoumo) <- as.character(c(6:7,13:14,20:21,27:28))
tem_jieguo <- bind_cols(tem_zhounei,tem_zhoumo) %>% as.data.table() %>% setcolorder(c('姓名','性别',as.character(c(1:28))))

row_sel <- which(rowSums(is.na(tem_jieguo))!=2)
rows_cont <- tem_jieguo[which(rowSums(is.na(tem_jieguo))!=2),]
col_sel <- which(is.na(tem_jieguo[which(rowSums(is.na(tem_jieguo))!=2),]))
rows_cont[1,col_sel[3]] <- '早'
rows_cont[1,col_sel[4]] <- '早'

rows_cont[1,col_sel[3]] <- '早'
rows_cont[1,col_sel[4]] <- '早'
rows_cont[1,col_sel[3]] <- '早'
rows_cont[1,col_sel[4]] <- '早'
tem_jieguo[row_sel] <- rows_cont

which(rowSums(is.na(tem_jieguo))!=2)
person_da[order(-性别)]
# out put jieguo ----
write.csv(tem_jieguo,'clipboard')
