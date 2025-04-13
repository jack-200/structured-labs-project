# Import libraries and configure logging
import pandas as pd
import plotly.express as px
import logging
from preswald import text, plotly, connect, get_df, table, checkbox, selectbox

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Display introductory text
text("# Welcome to Preswald! 🎉")
text("## Dataset Overview")
text("Explore the dataset with filters and visualizations. 📊")
text("**Columns:** Vegetable, Form, RetailPrice, RetailPriceUnit, Yield, CupEquivalentSize, CupEquivalentUnit, and CupEquivalentPrice.")

# Load dataset and log initial rows
connect()
try:
    data = get_df("vegetable_prices_csv")
    logging.info("First two rows of the dataset:\n%s", data.head(2).to_string())
except ValueError as e:
    logging.error("Configuration error: %s", e)
except Exception as e:
    logging.error("Error retrieving data: %s", e)

# Filter and visualize fresh vegetables
text("### Fresh Vegetables: Scatter Plot")
fresh_data = data[data["Form"] == "Fresh"].sort_values(by="RetailPrice", ascending=True)
show_labels = checkbox("Show Labels", default=False)
scatter_fig = px.scatter(
    fresh_data,
    x="Vegetable",
    y="RetailPrice",
    text="Vegetable" if show_labels else None,
    title="Fresh Vegetable Retail Prices (Scatter Plot)",
    labels={"Vegetable": "Vegetable", "RetailPrice": "Retail Price"},
)
scatter_fig.update_traces(textposition="top center", marker=dict(size=12, color="lightgreen"))
scatter_fig.update_layout(template="plotly_white")
plotly(scatter_fig)

# Filter by "Form" and sort by selected column
text("### Filter and Sort Data")
form_filter = selectbox("Select Form to Filter", options=data["Form"].unique().tolist(), default="Fresh")
filtered_data = data[data["Form"] == form_filter]
sort_column_options = [col for col in filtered_data.columns if col not in ["Vegetable", "Form", "RetailPriceUnit", "CupEquivalentUnit"]]
sort_column = selectbox("Select Column to Sort Top 10", options=sort_column_options, default="RetailPrice")
reverse_order = checkbox("Reverse Order", default=False)

# Visualize top 10 vegetables by selected column
top_10 = filtered_data.sort_values(by=sort_column, ascending=False).head(10)
if reverse_order:
    top_10 = top_10.iloc[::-1]
bar_fig = px.bar(
    top_10,
    x="Vegetable",
    y=sort_column,
    text=sort_column if show_labels else None,
    title=f"Top 10 Vegetables by {sort_column} (Bar Chart) - Form: {form_filter}",
    labels={"Vegetable": "Vegetable", sort_column: sort_column},
    color="Vegetable",
)
bar_fig.update_layout(template="plotly_white")
plotly(bar_fig)

# Display full dataset
text("### Full Dataset")
table(data)