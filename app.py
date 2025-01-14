import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc

# Load the data
df = pd.read_csv('Superstore.csv', encoding='latin1')

# Convert 'Order Date' to datetime
df['Order Date'] = pd.to_datetime(df['Order Date'])

# Extract year from 'Order Date'
df['Year'] = df['Order Date'].dt.year

# Dictionary to map full state names to abbreviations
state_abbreviations = {
    'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA',
    'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'Florida': 'FL', 'Georgia': 'GA',
    'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA',
    'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
    'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS',
    'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH',
    'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC',
    'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA',
    'Rhode Island': 'RI', 'South Carolina': 'SC', 'South Dakota': 'SD', 'Tennessee': 'TN',
    'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA',
    'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY'
}

# Convert full state names to abbreviations
df['State'] = df['State'].map(state_abbreviations)

# Initialize the Dash app with Bootstrap theme
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the layout of the dashboard
app.layout = dbc.Container([
    # Page d'accueil
    html.Div(id='home-page', children=[
        dbc.Row([
            dbc.Col(html.H1("Sales Analysis Dashboard", className="text-center my-4"), width=12)
        ]),
        
        # Filtres
        dbc.Row([
            dbc.Col([
                html.Label("Region", className="mb-2"),  # Texte descriptif pour le filtre des régions
                dcc.Dropdown(
                    id='region-dropdown',
                    options=[{'label': 'All', 'value': 'All'}] + [{'label': region, 'value': region} for region in df['Region'].unique()],
                    value='All',
                    placeholder="Select a region",
                    className="mb-3"
                ),
            ], width=6),
            dbc.Col([
                html.Label("Year", className="mb-2"),  # Texte descriptif pour le filtre des années
                dcc.Dropdown(
                    id='year-dropdown',
                    options=[{'label': 'All', 'value': 'All'}] + [{'label': year, 'value': year} for year in sorted(df['Year'].unique())],
                    value='All',
                    placeholder="Select a year",
                    className="mb-3"
                ),
            ], width=6),
        ]),
        
        # Indicateurs Clés (KPI)
        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.H4("Total Sales", className="card-title"),
                    html.H2(id='total-sales', className="card-text")
                ])
            ], color="primary", inverse=True), width=4),
            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.H4("Total Profits", className="card-title"),
                    html.H2(id='total-profits', className="card-text")
                ])
            ], color="success", inverse=True), width=4),
            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.H4("Avg Discount", className="card-title"),
                    html.H2(id='avg-discount', className="card-text")
                ])
            ], color="info", inverse=True), width=4),
        ], className="mb-4"),
        
        # Visualisations côte à côte
        dbc.Row([
            dbc.Col(dcc.Graph(id='sales-by-state-map'), width=6),
            dbc.Col(dcc.Graph(id='sales-by-month'), width=6),
        ]),
        
        # Bouton pour accéder aux autres visualisations
        dbc.Row([
            dbc.Col(html.Div(
                dbc.Button('Other Informations', id='other-info-button', color="secondary", className="mt-4"),
                className="text-center"
            ), width=12)
        ]),
    ]),
    
    # Page des autres visualisations
    html.Div(id='other-info-page', style={'display': 'none'}, children=[
        dbc.Row([
            dbc.Col(html.H1("Other Informations", className="text-center my-4"), width=12)
        ]),
        
        # Filtres
        dbc.Row([
            dbc.Col([
                html.Label("Region", className="mb-2"),  # Texte descriptif pour le filtre des régions
                dcc.Dropdown(
                    id='region-dropdown-other',
                    options=[{'label': 'All', 'value': 'All'}] + [{'label': region, 'value': region} for region in df['Region'].unique()],
                    value='All',
                    placeholder="Select a region",
                    className="mb-3"
                ),
            ], width=6),
            dbc.Col([
                html.Label("Year", className="mb-2"),  # Texte descriptif pour le filtre des années
                dcc.Dropdown(
                    id='year-dropdown-other',
                    options=[{'label': 'All', 'value': 'All'}] + [{'label': year, 'value': year} for year in sorted(df['Year'].unique())],
                    value='All',
                    placeholder="Select a year",
                    className="mb-3"
                ),
            ], width=6),
        ]),
        
        # Graphiques supplémentaires
        dbc.Row([
            dbc.Col(dcc.Graph(id='sales-by-category'), width=12),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(id='sales-by-subcategory'), width=12),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(id='profit-by-subcategory'), width=12),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(id='discount-by-category'), width=12),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(id='quantity-by-product'), width=12),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(id='performance-by-segment'), width=12),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(id='performance-by-shipmode'), width=12),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(id='sales-by-city'), width=12),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(id='profit-by-customer'), width=12),
        ]),
        
        # Bouton pour revenir à la page d'accueil
        dbc.Row([
            dbc.Col(html.Div(
                dbc.Button('Back to Home', id='back-to-home-button', color="secondary", className="mt-4"),
                className="text-center"
            ), width=12)
        ]),
    ]),
], fluid=True)

# Define the callback to update the graphs and KPIs
@app.callback(
    [Output('total-sales', 'children'),
     Output('total-profits', 'children'),
     Output('avg-discount', 'children'),
     Output('sales-by-state-map', 'figure'),
     Output('sales-by-month', 'figure'),
     Output('other-info-page', 'style'),
     Output('home-page', 'style'),
     Output('sales-by-category', 'figure'),
     Output('sales-by-subcategory', 'figure'),
     Output('profit-by-subcategory', 'figure'),
     Output('discount-by-category', 'figure'),
     Output('quantity-by-product', 'figure'),
     Output('performance-by-segment', 'figure'),
     Output('performance-by-shipmode', 'figure'),
     Output('sales-by-city', 'figure'),
     Output('profit-by-customer', 'figure')],
    [Input('region-dropdown', 'value'),
     Input('year-dropdown', 'value'),
     Input('other-info-button', 'n_clicks'),
     Input('back-to-home-button', 'n_clicks'),
     Input('region-dropdown-other', 'value'),
     Input('year-dropdown-other', 'value')]
)
def update_dashboard(selected_region, selected_year, other_info_clicks, back_to_home_clicks, selected_region_other, selected_year_other):
    # Initialize click counters if they are None
    if other_info_clicks is None:
        other_info_clicks = 0
    if back_to_home_clicks is None:
        back_to_home_clicks = 0
    
    # Determine which page to display
    if other_info_clicks > back_to_home_clicks:
        home_style = {'display': 'none'}
        other_info_style = {'display': 'block'}
    else:
        home_style = {'display': 'block'}
        other_info_style = {'display': 'none'}
    
    # Determine which filters to use based on the active page
    if home_style['display'] == 'block':
        region_filter = selected_region
        year_filter = selected_year
    else:
        region_filter = selected_region_other
        year_filter = selected_year_other
    
    # Filter the data based on the selected region and year
    filtered_df = df if region_filter == 'All' else df[df['Region'] == region_filter]
    filtered_df = filtered_df if year_filter == 'All' else filtered_df[filtered_df['Year'] == year_filter]
    
    # Calculate KPIs
    total_sales = filtered_df['Sales'].sum()
    total_profits = filtered_df['Profit'].sum()
    avg_discount = (filtered_df['Discount'] * filtered_df['Quantity']).sum() / filtered_df['Quantity'].sum()
    
    # Format KPIs
    kpi_sales = f"${total_sales:,.2f}"
    kpi_profits = f"${total_profits:,.2f}"
    kpi_discount = f"{avg_discount:.2%}"
    
    # Graph 1: Sales by State (Map)
    sales_by_state = filtered_df.groupby('State')['Sales'].sum().reset_index()
    fig1 = px.choropleth(
        sales_by_state,
        locations='State',
        locationmode='USA-states',
        color='Sales',
        scope='usa',
        title='Sales by State',
        color_continuous_scale='Viridis'
    )
    
    # Graph 2: Monthly Sales Over Time
    filtered_df['YearMonth'] = filtered_df['Order Date'].dt.to_period('M').astype(str)
    sales_by_month = filtered_df.groupby('YearMonth')['Sales'].sum().reset_index()
    fig2 = px.line(
        sales_by_month,
        x='YearMonth',
        y='Sales',
        title='Monthly Sales Over Time',
        labels={'YearMonth': 'Month', 'Sales': 'Total Sales'}
    )
    
    # Graph 3: Sales by Category (Tri décroissant)
    sales_by_category = filtered_df.groupby('Category')['Sales'].sum().reset_index()
    sales_by_category = sales_by_category.sort_values(by='Sales', ascending=False)  # Tri décroissant
    fig3 = px.bar(
        sales_by_category,
        x='Category',
        y='Sales',
        title='Sales by Category',
        color='Category'
    )
    
    # Graph 4: Sales by Sub-Category (Tri décroissant)
    sales_by_subcategory = filtered_df.groupby(['Sub-Category', 'Category'])['Sales'].sum().reset_index()
    sales_by_subcategory = sales_by_subcategory.sort_values(by='Sales', ascending=False)  # Tri décroissant
    fig4 = px.bar(
        sales_by_subcategory,
        x='Sub-Category',
        y='Sales',
        title='Sales by Sub-Category',
        color='Category'
    )
    
    # Graph 5: Profit by Sub-Category (Tri décroissant)
    profit_by_subcategory = filtered_df.groupby(['Sub-Category', 'Category'])['Profit'].sum().reset_index()
    profit_by_subcategory = profit_by_subcategory.sort_values(by='Profit', ascending=False)  # Tri décroissant
    fig5 = px.bar(
        profit_by_subcategory,
        x='Sub-Category',
        y='Profit',
        title='Profit by Sub-Category',
        color='Category'
    )
    
    # Graph 6: Average Discount by Category (Tri décroissant)
    discount_by_category = filtered_df.groupby('Category')['Discount'].mean().reset_index()
    discount_by_category = discount_by_category.sort_values(by='Discount', ascending=False)  # Tri décroissant
    fig6 = px.bar(
        discount_by_category,
        x='Category',
        y='Discount',
        title='Average Discount by Category'
    )
    
    # Graph 7: Top 10 Products by Quantity Sold (Tri décroissant)
    quantity_by_product = filtered_df.groupby('Product Name')['Quantity'].sum().reset_index()
    quantity_by_product = quantity_by_product.sort_values(by='Quantity', ascending=False).head(10)  # Tri décroissant
    fig7 = px.bar(
        quantity_by_product,
        x='Quantity',
        y='Product Name',
        orientation='h',
        title='Top 10 Products by Quantity Sold'
    )
    
    # Graph 8: Sales and Profit by Customer Segment (Tri décroissant)
    performance_by_segment = filtered_df.groupby('Segment').agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()
    performance_by_segment = performance_by_segment.sort_values(by='Sales', ascending=False)  # Tri décroissant
    fig8 = px.bar(
        performance_by_segment,
        x='Segment',
        y=['Sales', 'Profit'],
        barmode='group',
        title='Sales and Profit by Customer Segment'
    )
    
    # Graph 9: Sales and Profit by Ship Mode (Tri décroissant)
    performance_by_shipmode = filtered_df.groupby('Ship Mode').agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()
    performance_by_shipmode = performance_by_shipmode.sort_values(by='Sales', ascending=False)  # Tri décroissant
    fig9 = px.bar(
        performance_by_shipmode,
        x='Ship Mode',
        y=['Sales', 'Profit'],
        barmode='group',
        title='Sales and Profit by Ship Mode'
    )
    
    # Graph 10: Top 10 Cities by Sales (Tri décroissant)
    sales_by_city = filtered_df.groupby('City')['Sales'].sum().reset_index()
    sales_by_city = sales_by_city.sort_values(by='Sales', ascending=False).head(10)  # Tri décroissant
    fig10 = px.bar(
        sales_by_city,
        x='City',
        y='Sales',
        title='Top 10 Cities by Sales'
    )
    
    # Graph 11: Top 10 Customers by Profit (Tri décroissant)
    profit_by_customer = filtered_df.groupby('Customer Name')['Profit'].sum().reset_index()
    profit_by_customer = profit_by_customer.sort_values(by='Profit', ascending=False).head(10)  # Tri décroissant
    fig11 = px.bar(
        profit_by_customer,
        x='Customer Name',
        y='Profit',
        title='Top 10 Customers by Profit'
    )
    
    return kpi_sales, kpi_profits, kpi_discount, fig1, fig2, other_info_style, home_style, fig3, fig4, fig5, fig6, fig7, fig8, fig9, fig10, fig11

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)