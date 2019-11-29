library(tidyverse)
library(data.table)
library(stringi)
library(readxl)
library(arules)

# A[,.n,.(1，2.)]
# A[!DUPLICATED(A[1:2])]
#xlsx:

# dplyr::distinct()
# fread("F:\\20180806\\aproiri\\18S56\\data\\180730_180807.csv",encoding = 'UTF-8',skip=19)%>% as.data.table()
get_All_da <- function(base_path){
  all_paths <- base_path %>% list.files() %>% map_chr(function(x) return(str_c(stringi::stri_conv(base_path,"GBK","UTF-8"),stringi::stri_conv(x,"UTF-8"))))
  da_path <- data.table("paths" = all_paths)
  
  # for (i in c(1:length(all_paths))){
  #   print(all_paths[i])
  # test_da  <-fread(all_paths[i],encoding = 'UTF-8',skip=19)%>% as.data.table()
  # test_da[,":="(款号= as.character(款号)),]
  # colClasses_used <- sapply(test_da,class)
  # print(length(colClasses_used))
  # }
  
  
  da_path[,":="(submix = str_sub(paths,-3,-1)),]
  #  csv file 
  csv_paths_all <- da_path[submix=='csv',paths,]
  
  # type(colClasses_used)
  csv_paths_all_da  <-csv_paths_all %>%  map_df(function(x) return(fread(x,skip=19,encoding = 'UTF-8',colClasses = c('character','character','character','character',
                                                                                                                     'character','integer','integer','character',
                                                                                                                     'character', 'integer','character','integer',
                                                                                                                    'character','character','character','integer',
                                                                                                                    'character','numeric','numeric','numeric'
                                                                                                  )))) %>% as.data.table()
  
  csv_paths_all_da[,":="("款号"= as.character(款号)),]
  
  #  xls file
  xls_paths_all <- da_path[submix=='lsx',paths,]
  
  if (length(xls_paths_all) >0){
    xls_paths_all_da  <- xls_paths_all %>% map_df(function(x) {return(read_xlsx(x,sheet='分析 1',skip=3,col_types =c("text","text","text","text","text","numeric","numeric","text","text",
                                                                                                                   "numeric","text","numeric","text","text","text","text","numeric","numeric","numeric")))}) %>% as.data.table()
    
    Ori_da <- bind_rows(csv_paths_all_da,xls_paths_all_da) %>%as.data.table()
    rm(csv_paths_all_da,xls_paths_all_da)
    
  } else{
    
    
    Ori_da <- csv_paths_all_da %>%as.data.table()
    rm(csv_paths_all_da)
  }
  
  
  
  setnames(Ori_da,names(Ori_da),c('qudao','area','agent','provi','shopid','ymd','sellid','season','bigtype','bigtypeid','midtype','midtypeid',
                                  'smalltype','smalltypeid','sku','color','sex','lssl','lsje','lssz'))
  
  # rseason_pp <- fread("E:\\xh\\pp\\产品季节.txt") %>% setnames(c('产品季','新季节'),c("season","season_new"))
  # sku_pp <-  fread("E:\\xh\\pp\\引流款数据.txt") %>% setnames(c('商品编号','款属性'),c("sku","sku_yinlin"))
  # sku_pp[,":="(sku = as.character(sku)),]
  # 
  # 
  # Ori_da_A <- Ori_da %>% left_join(season_pp,by=c('season')) %>% left_join(sku_pp,by=c('sku'))  %>% as.data.table()
  # rm(Ori_da)
  
  Ori_da[,":="(unique_sellid = str_c(shopid,sellid,ymd,sep="-")),]
  Ori_da[,":="(sell_type = str_c(bigtype,midtype,smalltype,sex,sku,color,sep = '-')),]
  
  return (Ori_da)
}


get_All_Aproior_zouDa <- function(Read_da = Ori_da,support_Sel = NULL,confidence_Sel = NULL){
  Used_da <- Read_da[,.(unique_sellid,sell_type),]
  Used_da_apri_input <- Used_da[!duplicated(Used_da),,]
  if (dim(Used_da_apri_input)[1] ==0){
    return (NULL);
  }
  Ori_Trans <- as(Used_da_apri_input[,.(val = list(sell_type)),by=.(unique_sellid)][,.(val),][[1]],'transactions')
  
  if (is.null(support_Sel)){
    leng_item <- Read_da[,.N,]
    min_fre_item <- Read_da[,.N,by=.(sell_type)][order(N)][1,2]#求出单项最小支持度极端???
    max_fre_item <- Read_da[,.N,by=.(sell_type)][order(-N)][1,2]#求出单项最小支持度极端???
    min_fre_feq<- min_fre_item/leng_item
    max_fre_feq <- max_fre_item/leng_item
    # 28原则选择置信???
    # support_Sel <- as.vector(min_fre_feq +(max_fre_feq-min_fre_feq)/10*1)[[1]]
    support_Sel <- (as.vector(min_fre_feq +(max_fre_feq-min_fre_feq)/10*1)[[1]])^2
  }
  if (is.null(confidence_Sel)){
    confidence_Sel = support_Sel
  }
  # (Ori_Trans)@data@Dim[2] 事务的组合数和item
  # summary(Ori_Trans)
  Re_Ruels <- apriori(Ori_Trans,parameter = list(support = support_Sel,confidence = confidence_Sel,target="rules",maxlen=3))
?apriori
  length_rules <- (Re_Ruels)@rhs@data@Dim[2]
  if (length_rules >100000){
    tem_re <- as.data.table(as(Re_Ruels[1:50000],'data.frame'))
  }else{
    tem_re <- as.data.table(as(Re_Ruels,'data.frame'))
  }
  # 
  # 
  tem_re[,":="(rules = as.character(rules)),]
  tem_re[,":="(lhs = plyr::laply(rules,function (da){ return (str_split(da,' => ')[[1]][1])}),
               rhs = plyr::laply(rules,function (da){ return (str_split(da,' => ')[[1]][2])})),]

  # setcolorder(tem_re,c('tag','lhs','rhs','support','confidence','lift'))
  setcolorder(tem_re,c('lhs','rhs','support','confidence','lift'))
  # return(tem_re)
  
  return (tem_re)
}


deal_lhs_rhs <- function(x,type = 1){
  length_len <- nchar(x)
  if (length_len <=2){
    return ((NA))
  }else if(length_len>2){
    if(type == 1){
      return (str_split(str_sub((x),2,-2),'-')[[1]][1])
    }else if (type == 2){
      return (str_split(str_sub((x),2,-2),'-')[[1]][2])
    }else if(type == 3){
      return (str_split(str_sub((x),2,-2),'-')[[1]][3])
    }else if (type == 4 ){
      return (str_split(str_sub((x),2,-2),'-')[[1]][4])
    }else if (type == 5 ){
      return (str_split(str_sub((x),2,-2),'-')[[1]][5])
    }
    else if (type == 6 ){
      return (str_split(str_sub((x),2,-2),'-')[[1]][6])
    }
  }
}


get_Final_da <- function(data_x,support_Sel_ori = NULL,confidence_Sel_ori = NULL){
  tem_re <- data_x %>% get_All_Aproior_zouDa(support_Sel = support_Sel_ori,confidence_Sel = confidence_Sel_ori) %>% as.data.table()
  tem_split<- tem_re[,":="(lhs_sex= sapply(lhs,deal_lhs_rhs,4),
                           lhs_middle_rhs = sapply(lhs,deal_lhs_rhs,2),
                           lhs_sku = sapply(lhs,deal_lhs_rhs,5),
                           lhs_color = sapply(lhs,deal_lhs_rhs,6),
                           # lhs_neiwaida = sapply(lhs,deal_lhs_rhs,5),
                           rhs_sex= sapply(rhs,deal_lhs_rhs,4),
                           rhs_middle_rhs = sapply(rhs,deal_lhs_rhs,2),
                           rhs_sku = sapply(rhs,deal_lhs_rhs,5),
                           rhs_color = sapply(rhs,deal_lhs_rhs,6)
                           # ,
                           # rhs_neiwaida = sapply(rhs,deal_lhs_rhs,5)
  ),]
  
  tem_split <- as.data.table(tem_split)
  tem_split_out <-tem_split[!is.na(lhs_middle_rhs),,][,.(lhs_sex,lhs_middle_rhs,lhs_sku,lhs_color,rhs_sex,rhs_middle_rhs,rhs_sku,rhs_color,support,confidence,lift),]
  tem_split_out[,':='(lhs_color=str_replace(lhs_color,",服装","")),]
  
  tem_split_input <- tem_split_out
  tem_split_input[,":="(lhs_color = sapply(lhs_color,deal_color),rhs_color = sapply(rhs_color,deal_color)),]
  setorder(tem_split_input,lhs_sku,lhs_color,-support,-confidence,-lift)
  tem_split_input[,":="(intag =c(1:nrow(tem_split_input))),]
  tem_split_input[,":="(rank_sku_color = rank(intag,ties.method = 'first')),.(lhs_sku,lhs_color)]
  tem_split_input[,":="(intag = NULL),]
  
  return (tem_split_input)
  
}

deal_color <- function(x){
  len_x <- nchar(x)
  if (len_x==4){
    return(str_c(x))
  }else if(len_x==3){
    return (str_c("0",x))
  }else if(len_x==2){
    return (str_c("00",x))
  }else if(len_x==1){
    return (str_c("000",x))
  }else{
    return (str_c(x))
  }
}
# base_path <- 'C:\\Users\\hasee\\Desktop\\aproiri\\18S56\\data\\'
base_path <- 'F:\\20180806\\aproiri\\18S56\\data\\'
tem <- get_All_da(base_path) %>% as.data.table() 
tem[,.N,season]

tem[,.N,ymd][order(ymd)]
tem[,.N,season][order(season)]
tem[,.N,bigtype]

# filter data and concat type
# write.csv(tem[,.N,.(bigtype,midtype)],"clipboard")
tem <- tem[bigtype=='服装',,]
pp_type_new <- fread('C:\\Users\\hasee\\Desktop\\类型匹配.txt')

tem_re <- get_All_da(base_path) %>% as.data.table()  %>% get_All_Aproior_zouDa() 
tem_re <- tem %>% get_All_Aproior_zouDa() 

# str(tem_split_input)
# write.csv(tem_split_input,"C:\\Users\\hasee\\Desktop\\zouda_fs.txt")

# 
# tem_re[,unique(ymd),]
# tem_re[,unique(season),]
# # tem_re[season=="2018S7",,]
# deal_lhs_rhs("{配件-包-斜挎包-女-15058530003-134}",1) # big type
# deal_lhs_rhs("{配件-包-斜挎包-女-15058530003-134}",2) # mid type
# deal_lhs_rhs("{配件-包-斜挎包-女-15058530003-134}",3) # small type
# deal_lhs_rhs("{配件-包-斜挎包-女-15058530003-134}",4) # sex
# deal_lhs_rhs("{配件-包-斜挎包-女-15058530003-134}",5) # sku
# deal_lhs_rhs("{配件-包-斜挎包-女-15058530003-134}",6)# color
# 
tem_split<- tem_re[,":="(lhs_sex= sapply(lhs,deal_lhs_rhs,4),
             lhs_middle_rhs = sapply(lhs,deal_lhs_rhs,2),
             lhs_sku = sapply(lhs,deal_lhs_rhs,5),
             lhs_color = sapply(lhs,deal_lhs_rhs,6),
             # lhs_neiwaida = sapply(lhs,deal_lhs_rhs,5),
             rhs_sex= sapply(rhs,deal_lhs_rhs,4),
             rhs_middle_rhs = sapply(rhs,deal_lhs_rhs,2),
             rhs_sku = sapply(rhs,deal_lhs_rhs,5),
             rhs_color = sapply(rhs,deal_lhs_rhs,6)
             # ,
             # rhs_neiwaida = sapply(rhs,deal_lhs_rhs,5)
             ),]
tem_split <- as.data.table(tem_split)
tem_split_out <-tem_split[!is.na(lhs_middle_rhs),,][,.(lhs_sex,lhs_middle_rhs,lhs_sku,lhs_color,rhs_sex,rhs_middle_rhs,rhs_sku,rhs_color,support,confidence,lift),]
tem_split_out[,':='(lhs_color=str_replace(lhs_color,",服装","")),]
tem_split_out[,":="(lhs_sku=str_replace(lhs_sku,",配件","")),]
tem_split_out[,':='(rhs_color=str_replace(rhs_color,",服装","")),]
tem_split_out[,":="(rhs_sku=str_replace(rhs_sku,",配件","")),]
str(tem_split)
# write.csv(tem_split_out,'C:\\Users\\hasee\\Desktop\\zouda_0807.csv')
# tem_split_input <- fread('C:\\Users\\hasee\\Desktop\\zouda_0807.csv')
tem_split_input <- tem_split_out
# 
# 

# 
# # deal_color("20")
# 
tem_split_input[,":="(lhs_color = sapply(lhs_color,deal_color),rhs_color = sapply(rhs_color,deal_color)),]
setorder(tem_split_input,lhs_sku,lhs_color,-support,-confidence,-lift)
tem_split_input[,":="(intag =c(1:nrow(tem_split_input))),]
tem_split_input[,":="(rank_sku_color_support = rank(intag,ties.method = 'first')),.(lhs_sku,lhs_color)]
tem_split_input[,":="(intag = NULL),]

pp_type_new <- fread('C:\\Users\\hasee\\Desktop\\类型匹配.txt')
setnames(pp_type_new,c('midtype','TYPE_S_X'),c('lhs_middle_rhs','lhs_middle_S_X'))
setnames(pp_type_new,c('midtype','TYPE_S_X'),c('rhs_middle_rhs','rhs_middle_S_X'))

tem_split_input <- tem_split_input %>% left_join(pp_type_new[,2:3],by=c('lhs_middle_rhs')) %>% as.data.table()

pp_type_new <- fread('C:\\Users\\hasee\\Desktop\\类型匹配.txt')
setnames(pp_type_new,c('midtype','TYPE_S_X'),c('rhs_middle_rhs','rhs_middle_S_X'))
tem_split_input <- tem_split_input %>% left_join(pp_type_new[,2:3],by=c('rhs_middle_rhs')) %>% as.data.table()

# only Shang
tem_split_input[lhs_middle_S_X=='上装'&(lhs_middle_rhs!=rhs_middle_rhs),,]
tem_split_input[lhs_middle_S_X=='上装'&rhs_middle_S_X=='下装',,]
# only xia
tem_split_input[lhs_middle_S_X=='下装'&(rhs_middle_S_X=='上装'),,]

tem_Da <- 
bind_rows(
  tem_split_input[(lhs_middle_S_X=='上装')&(rhs_middle_S_X=='上装')&(lhs_middle_rhs!=rhs_middle_rhs),,],
  tem_split_input[(lhs_middle_S_X=='上装')&(rhs_middle_S_X=='下装')&(lhs_middle_rhs!=rhs_middle_rhs),,],
  tem_split_input[(lhs_middle_S_X=='下装')&(rhs_middle_S_X=='上装')&(lhs_middle_rhs!=rhs_middle_rhs),,]
)
tem_split_input <- tem_Da[!duplicated(tem_Da)]
# unique(tem_re$lhs_neiwaida)
# unique(tem_re$color)
# tem_split_input[lhs_sku=="18058041904",,]
 
# str(tem_split_input)
# write.csv(tem_split_input,"C:\\Users\\hasee\\Desktop\\zouda_fs.txt")
# write.csv(tem_split_input,'F:\\20180806\\aproiri\\18S56\\data\\lele_0820.csv')
# tem_split_input <- fread('F:\\20180806\\aproiri\\18S56\\data\\lele_0820.csv')
# str(tem_split_input)
setorder(tem_split_input,lhs_sku,lhs_color,-support,-confidence,-lift)
# tem_split_input[,,][order(lhs_sku,lhs_color,support)]
# xlsx::write.xlsx(tem_split_input,"F:\\20180806\\aproiri\\18S56\\data\\lele_0820.xlsx")
# tem_split_input <- xlsx::read.xlsx("F:\\20180806\\aproiri\\18S56\\data\\lele_0820.xlsx",sheetIndex = 1)
tem_split_input <- tem_split_input[,,][order(lhs_sku,lhs_color,-support)]
tem_split_input_used<- tem_split_input[lhs_middle_rhs!=rhs_middle_rhs,,]
tem_split_input_used[,":="(rank_sku_color_support = frank(-support,ties.method = 'first')),.(lhs_sku,lhs_color)]
tem_split_input_used <- tem_split_input_used[rank_sku_color_support<=20,,]
tem_split_input_used<- tem_split_input_used[,,][order(lhs_sku,lhs_color,-lift)]
tem_split_input_used[,':='(rank_sku_color_support=NULL),]
tem_split_input_used[,":="(rank_sku_color_lift = frank(-lift,ties.method = 'first')),.(lhs_sku,lhs_color)]
# fivenum(tem_Da[,confidence,])
# tem_Da[confidence==1,,]
xlsx::write.xlsx(tem_split_input_used,"F:\\20180806\\aproiri\\18S56\\data\\aprior_before30_0826.xlsx")
#---- xiapo tag
tem
