library(DBI)
library(RSQLite)
library(dplyr)
library(ggplot2)
library(readr)
library(tidyverse)
library(irr)
library(psych)
library(purrr)

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

# Inter-rater data
filtered_data <- ranking_data %>%
  group_by(session_id) %>%
  filter(n() == 50) %>% 
  ungroup()

rater_summary <- ranking_data %>%
  group_by(session_id) %>%
  summarise(
    rater_mean   = mean(ranking, na.rm = TRUE),
    rater_median = median(ranking, na.rm = TRUE),
    rater_sd     = sd(ranking, na.rm = TRUE),
    rater_count     = n()
  )

individual_ratings <- filtered_data %>%
  select(session_id, image_name, ranking) %>%
  pivot_wider(
    names_from = session_id,
    values_from = ranking
  )

session_ids <- colnames(individual_ratings)[-1]
  
# Export rater data
write_csv(rater_summary, "~/../Thesis/rater_data.csv")

# Weighted Kappa
fleiss_kappa <- kappam.fleiss(ratings_wide[ , -1])

per_rater_kappa <- map_df(session_ids, function(r) {
  
  session_id <- individual_ratings[[r]]
  
  group_mean <- individual_ratings %>%
    select(-image_name, -all_of(r)) %>%
    rowMeans(na.rm = TRUE)
  
  group_ord <- round(group_mean / 10) * 10
  
  kappa_val <- kappa2(
    cbind(session_id, group_ord),
    weight = "squared"
  )$value
  
  tibble(
    session = r,
    kappa_with_group = kappa_val
  )
})

# ICC
icc <- ICC(individual_ratings[ , -1])
icc_table <- icc$results

per_rater_icc <- map_df(session_ids, function(r) {
  
  session_id <- individual_ratings[[r]]
  
  group_mean <- individual_ratings %>%
    select(-image_name, -all_of(r)) %>%
    rowMeans(na.rm = TRUE)
  
  mat <- cbind(session_id, group_mean)
  
  icc_val <- ICC(mat)$results
  
  tibble(
    rater = r,
    ICC11 = icc_val["ICC1", "ICC"],
    ICC21_aa = icc_val["ICC2", "ICC"],
    ICC21_c = icc_val["ICC3", "ICC"],
    ICC1k = icc_val["ICC1k", "ICC"],
    ICC2k_aa = icc_val["ICC2k", "ICC"],
    ICC2k_c = icc_val["ICC3k", "ICC"]
  )
})

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