library(DBI)
library(RSQLite)
library(dplyr)
library(ggplot2)
library(readr)
library(tidyverse)
library(irr)
library(psych)
library(purrr)
library(ggrepel)

con <- dbConnect(SQLite(), "../thesis_uv_website/chatbot_database.sqlite3")
ranking_data <- dbReadTable(con, 'avatar_ranking_imageranking')

# Inter-rater data
rater_summary <- ranking_data %>%
  group_by(session_id) %>%
  summarise(
    rater_mean   = mean(ranking, na.rm = TRUE),
    rater_median = median(ranking, na.rm = TRUE),
    rater_sd     = sd(ranking, na.rm = TRUE),
    rater_count     = n()
  ) %>%
  dplyr::mutate(rater_index = dplyr::row_number())


#filtered_raters <- rater_summary %>%
#  filter(rater_count >= 10) %>%
#  select(session_id)
#
#filtered_ranking_data <- ranking_data %>%
#  filter(session_id %in% filtered_raters$session_id)

filtered_ranking_data <- ranking_data %>%
  group_by(session_id) %>%
  filter(n() == 50) %>% 
  ungroup()

individual_ratings <- filtered_ranking_data %>%
  select(session_id, image_name, ranking) %>%
  pivot_wider(
    names_from = session_id,
    values_from = ranking
  )

session_ids <- colnames(individual_ratings)[-1]

# Export rater data
write_csv(rater_summary, "~/../Thesis/rater_data.csv")

# Rater Mean vs. SD Plot
ggplot(rater_summary, aes(x = rater_mean, y = rater_sd)) +
  geom_point(size = 3, alpha = 0.7) +
  geom_text_repel(
    aes(label = rater_count),
    size = 3,
    max.overlaps = Inf
  ) +
labs(
  x = "Participant's Mean Human Likeness Ranking",
  y = "Participant's Human Likeness Ranking Std Dev",
  title = "Participant's Human Likeness Ranking Mean vs. Std Dev",
  subtitle = "Point Label = Participant's Number of Rankings"
) +
  theme_minimal()
# Rater Median vs. SD Plot
ggplot(rater_summary, aes(x = rater_median, y = rater_sd)) +
  geom_point(size = 3, alpha = 0.7) +
  geom_text_repel(
    aes(label = rater_count),
    size = 3,
    max.overlaps = Inf
  )

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

# Mean and median with no normalization

ranking_results <- ranking_data %>%
  group_by(image_name) %>%
  summarise(
    mean = mean(ranking),
    sd   = sd(ranking),
    median = median(ranking),
    mad = mad(ranking),
    n      = n()
  )

filtered_ranking_results <- filtered_ranking_data %>%
  group_by(image_name) %>%
  summarise(
    mean = mean(ranking),
    sd   = sd(ranking),
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

ggplot(filtered_ranking_results, aes(x = mean)) +
  geom_histogram(
    breaks = seq(10, 100, by = 10),
    color = "white"
  ) +
  theme_minimal() +
  labs(
    title = "Mean Human Likness Distribution of Image Dataset \nWithout Standardization",
    x = "Mean Human Likeness",
    y = "Count"
  )

ggplot(ranking_results, aes(x = reorder(image_name, mean), y = mean)) +
  geom_col(fill = "light grey") +
  geom_errorbar(
    aes(ymin = mean - sd, ymax = mean + sd)
  )

ggplot(filtered_ranking_results, aes(x = reorder(image_name, mean), y = mean)) +
  geom_col(fill = "light grey") +
  geom_errorbar(
    aes(ymin = mean - sd, ymax = mean + sd)
  )

# Median Plots
ggplot(ranking_results, aes(x = median)) +
  geom_histogram(
    breaks = seq(10, 100, by = 10),
    color = "white"
  )

ggplot(filtered_ranking_results, aes(x = median)) +
  geom_histogram(
    breaks = seq(10, 100, by = 10),
    color = "white"
  )

ggplot(ranking_results, aes(x = reorder(image_name, median), y = median)) +
  geom_col(fill = "light grey") +
  geom_errorbar(
    aes(ymin = median - mad, ymax = median + mad)
  )

ggplot(filtered_ranking_results, aes(x = reorder(image_name, median), y = median)) +
  geom_col(fill = "light grey") +
  geom_errorbar(
    aes(ymin = median - mad, ymax = median + mad)
  )

# Mean vs SD Scatter
ggplot(ranking_results, aes(x = mean, y = sd)) +
  geom_point(size = 3, alpha = 0.7) +
  geom_text_repel(
    aes(label = image_name),
    size = 3,
    max.overlaps = Inf
  ) +
  labs(
    x = "Image Mean Human Likeness Ranking",
    y = "Image Human Likeness Ranking Std Dev",
    title = "Image Human Likeness Ranking Mean vs. Std Dev",
    subtitle = "Data Point Label = Image Name"
  ) +
  theme_minimal()

# Median vs SD Scatter
ggplot(ranking_results, aes(x = median, y = sd)) +
  geom_point(size = 3, alpha = 0.7) +
  geom_text_repel(
    aes(label = image_name),
    size = 3,
    max.overlaps = Inf
  )

# Mean with within-rater normalization
ranking_z_scores <- ranking_data %>%
  group_by(session_id) %>%
  mutate(
    rating_z = (ranking - mean(ranking)) / sd(ranking)
  ) %>%
  ungroup()

filtered_ranking_z_scores <- filtered_ranking_data %>%
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

filtered_ranking_norm <- filtered_ranking_z_scores %>%
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
    )
  )

filtered_ranking_norm_results <- filtered_ranking_norm %>%
  mutate(
    mean_bin = cut(
      mean_z,
      breaks = 10,
      labels = FALSE
    )
  )

# Mean Plots
ggplot(ranking_norm_results, aes(x = mean_bin)) +
  geom_histogram(
    color = "white"
  )

ggplot(filtered_ranking_norm_results, aes(x = mean_bin)) +
  geom_bar(width = 0.95) +
  theme_minimal() +
  labs(
    title = "Mean Human Likness Distribution of Image Dataset \nWith Participant Z-Score Standardization",
    x = "Mean Human Likeness",
    y = "Count"
  )

ggplot(ranking_norm, aes(x = reorder(image_name, mean_z), y = mean_z)) +
  geom_col( fill = "light grey") +
  geom_errorbar(
    aes(ymin = mean_z - sd_z, ymax = mean_z + sd_z)
  )

ggplot(filtered_ranking_norm, aes(x = reorder(image_name, mean_z), y = mean_z)) +
  geom_col(fill = "light grey") +
  geom_errorbar(
    aes(ymin = mean_z - sd_z, ymax = mean_z + sd_z)
  )

