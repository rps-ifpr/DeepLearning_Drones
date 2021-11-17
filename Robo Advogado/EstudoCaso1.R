# Estudo de Caso 1 - Features Engineering com 
# VariÃ¡veis CategÃricas na PrÃ¡tica

# Definindo o diretÃ³rio de trabalho
setwd("e:/MachineLearning/Cap2")
getwd()

# Os modelos de aprendizado de mÃ¡quina tÃªm dificuldade em interpretar dados categÃ³ricos; 
# Mas a engenharia de recursos nos permite re-contextualizar nossos dados categÃ³ricos para 
# melhorar o rigor de nossos modelos de Machine Learning. A engenharia de recursos tambÃ©m 
# fornece camadas adicionais de perspectiva para a anÃ¡lise de dados. A grande questÃ£o que as 
# abordagens de engenharia de recursos resolvem Ã©: como utilizar meus dados de maneiras 
# interessantes e inteligentes para tornÃ¡-los muito mais Ãºteis? 

# A engenharia de recursos nÃ£o trata de limpar dados, remover valores nulos ou outras tarefas 
# semelhantes (isso Ã© Data Wrangling); a engenharia de recursos tem a ver com a alteraÃ§Ã£o de 
# variÃ¡veis para melhorar a histÃ³ria que elas contam. 

# Vejamos alguns exemplos de tarefas de engenharia de atributos!

# Para este estudo de caso usaremos este dataset com dados bancÃ¡rios de usuÃ¡rios:

# Dataset: http://archive.ics.uci.edu/ml/machine-learning-databases/00222/bank.zip

# Carregando os dados
dataset_bank <- read.table("bank/bank-full.csv", header = TRUE, sep = ";")
View(dataset_bank)

# Exemplo 1 - Criação de Nova Coluna

# Muitas vezes, quando vocÃª usa dados categÃ³ricos como preditores, pode achar que alguns dos 
# nÃ­veis dessa variÃ¡vel tÃªm uma ocorrÃªncia muito escassa ou que os nÃ­veis das variÃ¡veis sÃ£o 
# seriamente redundantes.

# Qualquer decisÃ£o que vocÃª tome para comeÃ§ar a agrupar os nÃ­veis de variÃ¡veis deve ser 
# estrategicamente orientada. Um bom comeÃ§o aqui para ambas as abordagens Ã© a funÃ§Ã£o table() em R.
table(dataset_bank$job)

# A ideia seria identificar a ocorrÃªncia de um nÃ­vel com poucos registros ou alternativamente 
# compartimentos que parecem mais indicativos do que os dados estÃ£o tentando informar.

# Ãs vezes, uma tabela Ã© um pouco mais difÃ­cil de ingerir; portanto, jogar isso em um grÃ¡fico 
# de barras pode ser mais fÃ¡cil.
library(dplyr)
library(ggplot2)

dataset_bank %>%
  group_by(job)%>%
  summarise(n = n())%>%
  ggplot(aes(x = job, y = n))+
  geom_bar(stat = "identity")+
  theme(axis.text.x = element_text(angle = 90, hjust = 1))

# Para esse estudo de caso, digamos que realmente queremos entender a profissÃ£o (job) de acordo 
# com o uso da tecnologia em uma determinada funÃ§Ã£o. Nesse caso, comeÃ§arÃ­amos a classificar 
# cada uma das profissÃµes em nÃ­vel mÃ©dio, alto e baixo em termos de uso de tecnologia.

# Uma funÃ§Ã£o que vocÃª pode usar Ã© a mutate do dplyr Ã© muito Ãºtil quando vocÃª estÃ¡ reatribuindo 
# muitos nÃ­veis diferentes de uma variÃ¡vel, em vez de usar alguma funÃ§Ã£o ifelse aninhada. 
# Essa funÃ§Ã£o tambÃ©m Ã© muito Ãºtil ao converter variÃ¡veis numÃ©ricas em dados categÃ³ricos. 

dataset_bank <- dataset_bank %>%
  mutate(technology_use = 
           case_when(job == 'admin' ~ "medio",
                     job == 'blue-collar' ~ "baixo",
                     job == 'entrepreneur' ~ "alto",
                     job == 'housemaid' ~ "baixo",
                     job == 'management' ~ "medio",
                     job == 'retired' ~ "baixo",
                     job == 'self-employed' ~ "baixo",
                     job == 'services' ~ "medio",
                     job == 'student' ~ "alto",
                     job == 'technician' ~ "alto",
                     job == 'unemployed' ~ "baixo",
                     job == 'unknown' ~ "baixo"))

View(dataset_bank)

# Como vocÃª pode ver acima, criamos um novo campo chamado technology_use e atribuÃ­mos a cada 
# um valor de acordo com seu uso de tecnologia. Tenho certeza de que vocÃª poderia argumentar 
# tarefas diferentes para cada uma delas, mas para este estudo de caso Ã© suficiente.

# Agora vamos revisar rapidamente esse novo campo.
table(dataset_bank$technology_use)

# Vamos colocar isso em percentual
round(prop.table(table(dataset_bank$technology_use)),2)


# A distribuiÃ§Ã£o deve depender do que vocÃª estÃ¡ tentando entender. Digamos que a granularidade 
# do trabalho foi muito maior e tivemos vÃ¡rios jobs relacionados a marketing, analista de marketing, 
# gerente de marketing digital etc.
# Aproveite a tabela e os grÃ¡ficos de barras para obter uma melhor 
# classificaÃ§Ã£o de nÃ­veis das variÃ¡veis.


# Exemplo 2 - VariÃveis Dummies 

# A coluna default representa se um usuÃ¡rio entreou ou nÃ£o no cheque especial.
# Em vez de deixar os nÃ­veis da variÃ¡vel padrÃ£o como "sim" e "nÃ£o", 
# codificaremos como uma variÃ¡vel fictÃ­cia (dummy). 

# Uma variÃvel dummy Ã© a representaÃ§Ã£o numÃ©rica de uma variÃ¡vel categÃ³rica. 
# Sempre que o valor padrÃ£o for sim, codificaremos para 1 e 0 caso contrÃ¡rio. 
# Para duas variÃ¡veis de nÃ­vel mutuamente exclusivas, isso elimina a necessidade de uma 
# coluna adicional, pois estÃ¡ implÃ­cito na primeira coluna.
dataset_bank <- dataset_bank %>%    
  mutate(defaulted = ifelse(default  == "yes", 1, 0))

View(dataset_bank)


# Exemplo 3 - One-Hot Encoding -

# Falamos sobre a criaÃ§Ã£o de uma Ãºnica coluna como uma variÃ¡vel dummy, mas devemos falar 
# sobre a codificaÃ§Ã£o one-hot. 

# Uma codificaÃ§Ã£o One-Hot Ã© efetivamente a mesma coisa que fizemos no item anterior, mas para variÃ¡veis 
# de muitos nÃ­veis em que a coluna possui 0s em todas as linhas, exceto onde o valor corresponde 
# Ã  nova coluna, que seria 1.

# Seria algo assim:

# 0000000001 - indica um valor
# 0000000010 - indica outro valor

library(caret)
?dummyVars
dmy <- dummyVars(" ~ .", data = dataset_bank)
bank.dummies <- data.frame(predict(dmy, newdata = dataset_bank))
View(bank.dummies)

# Acima, carregamos o pacote caret, executamos a funÃ§Ã£o dummyVars para todas as variÃ¡veis e, 
# em seguida, criamos um novo dataframe, dependendo das variÃ¡veis codificadas identificadas.
# Vamos dar uma olhada na nova tabela:
View(dataset_bank)
str(bank.dummies)
View(bank.dummies)


# NÃ£o incluÃ­mos todas as colunas, e vocÃª pode ver que isso deixou a coluna idade (age) no formato original.


# Exemplo 4 - Combinando Recursos ou Cruzamento de Recursos

# O cruzamento de recursos Ã© onde vocÃª combina diversas variÃ¡veis. 
# Ãs vezes, a combinaÃ§Ã£o de variÃ¡veis pode produzir um desempenho preditivo que executa o 
# que eles poderiam fazer isoladamente.

# Assim, podemos fazer um agrupamento por duas variÃ¡veis por exemplo, com a devida contagem:

dataset_bank %>% 
  group_by(job, marital) %>%
  summarise(n = n())


# Uma visualizaÃ§Ã£o disso geralmente Ã© muito mais fÃ¡cil de interpretar
dataset_bank %>% 
  group_by(job, marital) %>%
  summarise(n = n()) %>%
  ggplot(aes(x = job, y = n, fill = marital))+
  geom_bar(stat = "identity", position = "dodge") +
  theme(axis.text.x = element_text(angle = 90, hjust = 1))


# Uma avaliaÃ§Ã£o que geralmente Ã© muito mais fÃ¡cil de interpretar
dmy <- dummyVars( ~ job:marital, data = dataset_bank)
bank.cross <- predict(dmy, newdata = dataset_bank)
View(bank.cross)

# Lembre-se de que, ao combinar diversas variÃ¡veis, vocÃª pode ter alguns desses novos valores 
# muito esparsos. Revise as saÃ­das e se necessÃ¡rio aplique alguma outra tÃ©cnica mencionada anteriormente.


# ConclusÃ£o

# Existem muitos mÃ©todos adicionais que podem ser usados para variÃ¡veis numÃ©ricas e combinaÃ§Ãµes de 
# numÃ©rico e categÃ³rico; podemos usar o PCA, entre outras coisas, para melhorar o poder preditivo das 
# variÃ¡veis explicativas.




