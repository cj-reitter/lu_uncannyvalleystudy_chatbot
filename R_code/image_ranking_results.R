library(DBI)
library(RSQLite)
library(dplyr)
library(ggplot2)

con <- dbConnect(SQLite(), "../Thesis/lu_uncannyvalleystudy_chatbot/thesis_uv_website/chatbot_database.sqlite3")
ranking_data <- dbReadTable(con, 'avatar_ranking_imageranking')

# Mean and standard deviation with no normilization
ranking_results <- ranking_data %>%
  group_by(image_name) %>%
  summarise(
    mean = mean(ranking),
    sd_z   = sd(ranking),
    n      = n()
  )

ggplot(ranking_results, aes(x = mean)) +
  geom_histogram(
    breaks = seq(10, 100, by = 10),
    color = "white"
  )


# Mean and standard deviation with within-user normalization
ranking_z_scores <- ranking_data %>%
  group_by(session_id) %>%
  mutate(
    rating_z = (ranking - mean(ranking)) / sd(ranking)
  ) %>%
  ungroup()

ranking_norm <- ranking_z_scores %>%
  group_by(image_name) %>%
  summarise(
    mean_z = mean(rating_z),
    sd_z   = sd(rating_z),
    n      = n()
  )

# Sorts mean z-scores into 10 bins
ranking_norm <- ranking_norm %>% filter(!is.na(mean_z))

ranking_norm_results <- ranking_norm %>%
  mutate(
    bin = cut(
      mean_z,
      breaks = 10,
      labels = FALSE
    )
  )

ggplot(ranking_norm_results, aes(x = bin)) +
  geom_histogram(
    color = "white"
  )
