if (!require("vader")) install.packages("vader")
library(vader)
library(tidyverse)

d <- read_csv('transcripts.csv')
sentiment <- vader_df(d$content)

d <- d %>% 
  cbind(sentiment %>% select(compound, pos, neg)) %>% 
  tibble()

d
