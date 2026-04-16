# Scikit Learn Reference — LearnPythonStatsEcon

> Quick-reference for **Scikit Learn** in LearnPythonStatsEcon.
> This is a lightweight reference file, not a full agent.

---

## Official Documentation

https://scikit-learn.org/stable/api/index.html

## Key API Surface

Estimator API: .fit(X, y), .predict(X), .transform(X), .fit_transform(X); linear models: LinearRegression, Ridge, Lasso, LogisticRegression; preprocessing: StandardScaler, MinMaxScaler, OneHotEncoder, LabelEncoder; model selection: train_test_split, cross_val_score, GridSearchCV, KFold; metrics: mean_squared_error, r2_score, accuracy_score, classification_report; pipeline: Pipeline, make_pipeline

## Common Patterns & Pitfalls

Always split train/test before fitting: X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42). Use Pipeline to chain preprocessing + model: Pipeline([('scaler', StandardScaler()), ('model', LinearRegression())]). cross_val_score(model, X, y, cv=5) for robust generalisation estimates. Pitfall: fit the scaler on training data only, then transform both train and test — never call .fit_transform() on the test set.

## Key Conventions

- Follow project style rules when using Scikit Learn
- Refer to authority sources for API contract accuracy

## Related Agents

- `@technical-validator` — verify technical accuracy of Scikit Learn usage
- `@primary-producer` — implements code that depends on Scikit Learn
