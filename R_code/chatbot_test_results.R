library(DBI)
library(RSQLite)
library(dplyr)
library(ggplot2)
library(purrr)
library(broom)
library(psych)
library(ggimage)
library(magick)
library(rsq)
library(ggrepel)
library(ggforce)

# Connect to database
con <- dbConnect(SQLite(), "../thesis_uv_website/chatbot_database.sqlite3")
raw_data <- dbReadTable(con, 'thesis_survey_surveyresponse')

dbDisconnect(con)

# Remove duplicate responses
results <- raw_data %>%
  filter(!id %in% c(88,89,119))

# Age and Gender Analytics
results %>%
  summarise(
    n = sum(!is.na(age)),
    mean_age = mean(age, na.rm = TRUE),
    median_age = median(age, na.rm = TRUE)
  )

results %>%
  ggplot(aes(x = age)) +
  geom_histogram(binwidth = 5, color = "white") +
  labs(
    title = "Participant Age Distribution",
    x = "Participant Age",
    y = "Count"
  ) +
  theme_minimal() +
  theme(
    plot.title = element_text(hjust = 0.5)
  )

gender_counts <- results %>%
  count(gender, name = "n") %>%
  arrange(desc(n))

# Filter out participants with unsuitable oq responses 
results <- results %>%
  filter(!id %in% c(6, 26, 62))

like_items <- c(1,4,5,7,9,11,13,14,16,18,19)
all_items <- paste0("rq_", 1:20)

like_cols  <- paste0("rq_", like_items)

# Cronbach's alpha
alpha_results <- psych::alpha(results[ , like_cols], na.rm = TRUE)
alpha_results

section_ranges <- list(
  Overall = 1:5,
  Content = 6:10,
  Tone = 11:15,
  Avatar = 16:20
)

# Overall Regression

# Participant's mean answers for likeability and perceived intelligence
results <- results %>%
  mutate(
    likeability = rowMeans(select(., paste0("rq_", like_items)), na.rm = TRUE),
    intelligence = rowMeans(select(., all_of(all_items)) %>% select(-paste0("rq_", like_items)), na.rm = TRUE)
  )

# Center human_likeness for regressions
results <- results %>% mutate(hl_c = human_likeness - mean(human_likeness, na.rm = TRUE))

# Fit nested models predicting likeability
m1 <- lm(likeability ~ hl_c, data = results)
m2 <- lm(likeability ~ hl_c + I(hl_c^2), data = results)
m3 <- lm(likeability ~ hl_c + I(hl_c^2) + I(hl_c^3), data = results)

# Summaries
summary(m1)
summary(m2)
summary(m3)

r2_1 <- summary(m1)$r.squared
r2_2 <- summary(m2)$r.squared
r2_3 <- summary(m3)$r.squared

delta_r2_21 <- r2_2 - r2_1
delta_r2_32 <- r2_3 - r2_2
delta_r2_31 <- r2_3 - r2_1

cat("Delta R2 (2 vs 1):", delta_r2_21, "\n")
cat("Delta R2 (3 vs 2):", delta_r2_32, "\n")
cat("Delta R2 (3 vs 1):", delta_r2_31, "\n")

# Nested F-tests (sequential)
anova(m1, m2)   # tests whether adding quadratic term improves fit over linear
anova(m2, m3)   # tests whether adding cubic term improves fit over quadratic
anova(m1, m3)   # overall test

coefs <- summary(m3)$coefficients
# name of cubic term
cubic_name <- "I(hl_c^3)"
coefs[cubic_name, ]

t_cubic <- coefs[cubic_name, "t value"]
df_resid <- df.residual(m3)

# Two-sided p-value
p_two_sided <- 2 * pt(-abs(t_cubic), df_resid)

# One-sided p-value depending on alternative  beta3 > 0 
p_one_sided_alt_pos <- pt(t_cubic, df_resid, lower.tail = FALSE)

p_one_sided_alt_pos


newx <- seq(min(results$hl_c, na.rm = TRUE), max(results$hl_c, na.rm = TRUE), length.out = 200)
pred_df <- data.frame(hl_c = newx)

# Get predictions and standard errors once
pred_out <- predict(m3, newdata = pred_df, se.fit = TRUE)
pred_df$fit <- pred_out$fit
pred_df$se  <- pred_out$se.fit

# Back-transform to original human_likeness scale for plotting
pred_df$human_likeness <- pred_df$hl_c + mean(results$human_likeness, na.rm = TRUE)

# Confidence bands
pred_df <- pred_df %>%
  mutate(
    upr = fit + 1.96 * se,
    lwr = fit - 1.96 * se
  )

# Plot Overall Results
input_dir  <- "../thesis_uv_website/media"
output_dir <- "./media_small"

files <- list.files(input_dir, full.names = TRUE)

for (f in files) {
  img <- image_read(f)
  img_small <- image_scale(img, "150")   # width = 150px
  image_write(img_small, file.path(output_dir, basename(f)))}


ggplot(results, aes(x = human_likeness, y = likeability)) +
  geom_point() +
  geom_line(data = pred_df, aes(x = human_likeness, y = fit), color = "blue", size = 1, inherit.aes = FALSE) +
  geom_ribbon(data = pred_df, aes(x = human_likeness, ymin = lwr, ymax = upr), alpha = 0.2, inherit.aes = FALSE) +
  labs(x = "Human Likeness (10%-100%)", y = "Likeability (1-5)", title = "Cubic fit: Human Likeness vs. Likeability") +
  theme_minimal()

# Image Regression

image_results <- results %>%
  group_by(image_id) %>%
  summarise(
    likeability = mean(likeability, na.rm = TRUE),
    human_likeness = mean(human_likeness, na.rm = TRUE),
    n_x = n()
  )

mean_image_x <- mean(image_results$n_x, na.rm = TRUE)

image_results <- image_results %>%
  group_by(human_likeness) %>%
  arrange(likeability) %>%
  mutate(
    rank_y = row_number(),
    n_y = n(),
    likeability_jit_raw = likeability +
      (rank_y - (n_y + 1) / 2) * 0.07,
    likeability_jit = pmin(5, likeability_jit_raw),
    image_path = file.path(output_dir, paste0(image_id, ".jpg"))
  ) %>%
  ungroup()

ggplot(image_results, aes(x = human_likeness, y = likeability)) +
  geom_image(aes(image = image_path), size = 0.045) +
  labs(
    x = "Human Likeness (10%–100%)",
    y = "Average Likeability (1–5)",
    title = "Human Likeness vs. Average Likeability by Image"
  ) +
  theme_minimal()

ggplot(image_results, aes(x = human_likeness, y = likeability_jit)) +
  geom_image(aes(image = image_path), size = 0.045) +
  geom_line(data = pred_df, aes(x = human_likeness, y = fit), color = "blue", size = 1, inherit.aes = FALSE) +
  
  labs(
    x = "Human Likeness (10%–100%)",
    y = "Average Likeability (1–5)",
    title = "Human Likeness vs. Average Likeability by Image"
  ) +
  theme_minimal()

# Section-by-section Regression

results <- results %>%
  mutate(hl_c = human_likeness - mean(human_likeness, na.rm = TRUE)) %>%
  { 
    tmp <- .
    for(sec in names(section_ranges)) {
      idxs <- section_ranges[[sec]]
      rq_names <- paste0("rq_", idxs)
      like_in_sec <- intersect(paste0("rq_", like_items), rq_names)
      int_in_sec  <- setdiff(rq_names, like_in_sec)
      tmp <- tmp %>%
        mutate(
          !!paste0("like_", sec) := if(length(like_in_sec)>0) rowMeans(select(., all_of(like_in_sec)), na.rm = TRUE) else NA_real_,
          !!paste0("int_", sec)  := if(length(int_in_sec)>0)  rowMeans(select(., all_of(int_in_sec)), na.rm = TRUE)  else NA_real_
        )
    }
    tmp
  }

run_section_models <- function(data, yvar, predictor = "hl_c") {
  # build formulas
  f1 <- as.formula(paste(yvar, "~", predictor))
  f2 <- as.formula(paste(yvar, "~", predictor, "+ I(", predictor, "^2)"))
  f3 <- as.formula(paste(yvar, "~", predictor, "+ I(", predictor, "^2) + I(", predictor, "^3)"))
  # fit models
  m1 <- lm(f1, data = data)
  m2 <- lm(f2, data = data)
  m3 <- lm(f3, data = data)
  
  # R^2 values
  r2_1 <- summary(m1)$r.squared
  r2_2 <- summary(m2)$r.squared
  r2_3 <- summary(m3)$r.squared
  
  # nested anova p-values
  an13 <- anova(m1, m3)
  an23 <- anova(m2, m3)
  p_13 <- an13$`Pr(>F)`[2]
  p_23 <- an23$`Pr(>F)`[2]
  F_13 <- an13$F[2]
  F_23 <- an23$F[2]
  
  # coefficient table for m3
  coef_tab <- summary(m3)$coefficients
  # helper to safely extract values (returns NA if term not present)
  get_coef <- function(term, col) {
    if (term %in% rownames(coef_tab)) return(coef_tab[term, col])
    NA_real_
  }
  
  # extract cubic t and p-values (two-sided and one-sided)
  cubic_name <- "I(hl_c^3)"
  if (cubic_name %in% rownames(coef_tab)) {
    t_cubic <- coef_tab[cubic_name, "t value"]
    dfres <- df.residual(m3)
    p_two <- 2 * pt(-abs(t_cubic), dfres)                 # two-sided p
    p_one_pos <- pt(t_cubic, dfres, lower.tail = FALSE)   # one-sided for HA: beta3 > 0
    p_one_neg <- pt(t_cubic, dfres, lower.tail = TRUE)    # one-sided for HA: beta3 < 0
  } else {
    t_cubic <- NA_real_; p_two <- NA_real_; p_one_pos <- NA_real_; p_one_neg <- NA_real_
  }
  
  # extract coefficients for reporting
  out <- list(
    models = list(m1 = m1, m2 = m2, m3 = m3),
    r2 = c(r2_1 = r2_1, r2_2 = r2_2, r2_3 = r2_3),
    delta_r2_31 = r2_3 - r2_1,
    delta_r2_32 = r2_3 - r2_2,
    p_13 = p_13,
    p_23 = p_23,
    F_13 = F_13,
    F_23 = F_23,
    # cubic stats
    cubic_t = t_cubic,
    cubic_p_two = p_two,
    cubic_p_one_pos = p_one_pos,
    cubic_p_one_neg = p_one_neg,
    # coefficients for table
    intercept_est = get_coef("(Intercept)", "Estimate"),
    intercept_se  = get_coef("(Intercept)", "Std. Error"),
    intercept_t   = get_coef("(Intercept)", "t value"),
    intercept_p   = get_coef("(Intercept)", "Pr(>|t|)"),
    
    hl_est = get_coef("hl_c", "Estimate"),
    hl_se  = get_coef("hl_c", "Std. Error"),
    hl_t   = get_coef("hl_c", "t value"),
    hl_p   = get_coef("hl_c", "Pr(>|t|)"),
    
    quad_est = get_coef("I(hl_c^2)", "Estimate"),
    quad_se  = get_coef("I(hl_c^2)", "Std. Error"),
    quad_t   = get_coef("I(hl_c^2)", "t value"),
    quad_p   = get_coef("I(hl_c^2)", "Pr(>|t|)"),
    
    cubic_est = get_coef("I(hl_c^3)", "Estimate"),
    cubic_se  = get_coef("I(hl_c^3)", "Std. Error"),
    cubic_t   = t_cubic,
    cubic_p   = p_two
  )
  
  return(out)
}

# --- Run analyses for each section for the likeability composite ---
section_results <- map_dfr(names(section_ranges), function(sec) {
  yvar <- paste0("like_", sec)
  res <- run_section_models(results, yvar)
  
  tibble(
    section = sec,
    n = sum(!is.na(results[[yvar]])),
    R2_linear = res$r2["r2_1"],
    R2_quadratic = res$r2["r2_2"],
    R2_cubic = res$r2["r2_3"],
    deltaR2_3_vs_1 = res$delta_r2_31,
    deltaR2_3_vs_2 = res$delta_r2_32,
    p_3_vs_1 = res$p_13,
    p_3_vs_2 = res$p_23,
    F_13 = res$F_13,
    F_23 = res$F_23,
    
    # coefficients from m3
    intercept_est = res$intercept_est,
    intercept_se  = res$intercept_se,
    intercept_t   = res$intercept_t,
    intercept_p   = res$intercept_p,
    
    hl_est = res$hl_est,
    hl_se  = res$hl_se,
    hl_t   = res$hl_t,
    hl_p   = res$hl_p,
    
    quad_est = res$quad_est,
    quad_se  = res$quad_se,
    quad_t   = res$quad_t,
    quad_p   = res$quad_p,
    
    cubic_est = res$cubic_est,
    cubic_se  = res$cubic_se,
    cubic_t   = res$cubic_t,
    cubic_p_two_sided = res$cubic_p,
    
    # one-sided p-values for cubic: positive direction and negative direction
    cubic_p_one_pos = res$cubic_p_one_pos,
    cubic_p_one_neg = res$cubic_p_one_neg
  )
})


plots_by_section <- map(names(section_ranges), function(sec) {
  yvar <- paste0("like_", sec)
  if(sum(!is.na(results[[yvar]])) < 10) return(NULL)
  m3 <- lm(as.formula(paste(yvar, "~ hl_c + I(hl_c^2) + I(hl_c^3)")), data = results)
  newx <- seq(min(results$hl_c, na.rm = TRUE), max(results$hl_c, na.rm = TRUE), length.out = 200)
  pred_df <- data.frame(hl_c = newx)
  pr <- predict(m3, newdata = pred_df, se.fit = TRUE)
  pred_df <- pred_df %>%
    mutate(fit = pr$fit, se = pr$se.fit,
           upr = fit + 1.96*se, lwr = fit - 1.96*se,
           human_likeness = hl_c + mean(results$human_likeness, na.rm = TRUE))
  ggplot(results, aes_string(x = "human_likeness", y = yvar)) +
    geom_point(alpha = 0.6) +
    geom_line(data = pred_df, aes(x = human_likeness, y = fit), color = "blue", inherit.aes = FALSE) +
    geom_ribbon(data = pred_df, aes(x = human_likeness, ymin = lwr, ymax = upr), alpha = 0.2, inherit.aes = FALSE) +
    labs(title = "Cubic fit: Human Likeness vs. Likeability", subtitle = paste("Section:", sec), x = "Human Likeness (10%-100%)", y = "Likeability (1-5)") +
    theme_minimal()
})

# Plot Section plots
plots_by_section[[1]]
plots_by_section[[2]]
plots_by_section[[3]]
plots_by_section[[4]]

# Section Regression analysis
model_sections <- lm(like_Overall ~ like_Content + like_Tone + like_Avatar,
                     data = results)
standardized_b_model <- lm(scale(like_Overall) ~ scale(like_Content) + scale(like_Tone) +
     scale(like_Avatar), data = results)

summary(model_sections)
summary(standardized_b_model)

rsq.partial(model_sections)

# Age and Gender Analysis
model_age_mod <- lm(likeability ~ hl_c * age, data = results)
summary(model_age_mod)

model_gender_mod <- lm(likeability ~ hl_c * gender, data = results)
summary(model_gender_mod)
