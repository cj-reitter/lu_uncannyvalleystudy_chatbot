library(DBI)
library(RSQLite)
library(dplyr)
library(ggplot2)

con <- dbConnect(SQLite(), "../Thesis/lu_uncannyvalleystudy_chatbot/thesis_uv_website/chatbot_database.sqlite3")
ranking_data <- dbReadTable(con, 'avatar_ranking_imageranking')

# Mean and median with no normalization
ranking_results <- ranking_data %>%
  group_by(image_name) %>%
  summarise(
    mean = mean(ranking),
    sd_z   = sd(ranking),
    median = median(ranking),
    mad = mad(ranking),
    n      = n()
  )

# Mean Plots
ggplot(ranking_results, aes(x = mean)) +
  geom_histogram(
    breaks = seq(10, 100, by = 10),
    color = "white"
  )

ggplot(ranking_results, aes(x = reorder(image_name, mean), y = mean)) +
  geom_col(fill = "light grey") +
  geom_errorbar(
    aes(ymin = mean - sd_z, ymax = mean + sd_z)
  )

# Median Plots
ggplot(ranking_results, aes(x = median)) +
  geom_histogram(
    breaks = seq(10, 100, by = 10),
    color = "white"
  )

ggplot(ranking_results, aes(x = reorder(image_name, median), y = median)) +
  geom_col(fill = "light grey") +
  geom_errorbar(
    aes(ymin = median - mad, ymax = median + mad)
  )

# Mean with within-rater normalization
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
    mean_bin = cut(
      mean_z,
      breaks = 10,
      labels = FALSE
    ),
    median_bin = cut(
      median_z,
      breaks = 10,
      labels = FALSE
    )
  )

# Mean Plots
ggplot(ranking_norm_results, aes(x = mean_bin)) +
  geom_histogram(
    color = "white"
  )

ggplot(ranking_norm, aes(x = reorder(image_name, mean_z), y = mean_z)) +
  geom_col(fill = "light grey") +
  geom_errorbar(
    aes(ymin = mean_z - sd_z, ymax = mean_z + sd_z)
  )