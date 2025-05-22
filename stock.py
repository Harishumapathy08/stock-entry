import streamlit as st
import pandas as pd
import os
from io import BytesIO
from datetime import datetime
import calendar

FILE_NAME = "stock.xlsx"
SHEET_NAME = "PALLETS"

def calculate_closing_stock(opening, inward, outward):
    return opening + inward - outward

def get_days_in_month(year, month):
    return calendar.monthrange(year, month)[1]

def get_first_day_of_month(year, month):
    return calendar.weekday(year, month, 1)

# --- COMPLETE PRODUCT DATA STRUCTURE ---
product_data = {
    # 1. PALLET
    "PALLET": {
        "NORMAL PALLET": [
            "SAF-1210-IMH (LW)",
            "SAF-1210-IMH (HW)",
            "SAF-1210-3 IMP-V1",
            "SAF-1210-3 IMP-V2",
            "SAF-1210-LA2",
            "SAF-1212-IMH (HW)"
        ],
        "REINFORCEMENT PALLETS": [
            "SAF-1210-IMH (LW) 4M (LEG)",
            "SAF-1210-IMH (HW) 4M [DECK]",
            "SAF-PLAIN TOP 1210 9 LEG"
        ],
        "EXPORT PALLETS": [
            "SAF-1111-SL",
            "SAF-105105-SL",
            "SAF-1111-SL2",
            "SAF-1208",
            "N4-1210-LA2",
            "EN4-1210-V2 (Cold Storage Pallets)"
        ],
        "ROTO PALLETS": [
            "SAF ROTO-1210",
            "SAF ROTO-1208 (CHECKED TOP)"
        ],
        "SPILL PALLETS": [
            "SAF SPILLAGE PALLET - 4 DRUM",
            "SAF 2 Drum Spillage Pallets"
        ],
        "POLLY PALLETS": [
            "Polly Pallet"
        ]
    },

    # 2. DUSTBIN
    "DUSTBIN": {
        "Plastic": {
            "SAF Injection Moulded Litter Bins": ["60L", "80L", "110L"],
            "Wheel Waste Bin with Foot Pedal": ["120L", "240L"],
            "SAF Twin Bins": ["20L", "35L"],
            "SAF Roto Mold Bin": ["60L", "80L", "100L"],
            "SAF Primary Bin": ["50L", "80L"],
            "BMB": ["50L", "80L"],
            "PDL BINS": ["SAF PDL 60 LTR (LAMINAT)", "SAF PDL 10 LTR"]
        },
        "Metal": {
            "HDGI BINS": [
                "SAF HDGI BINS - 1100LTR",
                "SAF HDGI BINS - 1100LTR (DUROFLEX)",
                "SAF HDGI BINS - (1100L)with Padel",
                "SAF HDGI BINS - 660L",
                "SAF Metal Bin - (660L)(Powder Coating)"
            ],
            "RIC": ["SAF RIC 50 LTR"],
            "IRE": ["SAF IRE 35 LTR", "SAF IRE 80 LTR", "SAF IRE 100 LTR"]
        }
    },

    # 3. WATER TANK
    "WATER TANK": {
        "CV Tanks": ["30L", "50L", "100L", "200L", "500L", "1000L"],
        "MS Jumbo Container": ["400L"],
        "Intermediate Bulk Containers": ["1000L"],
        "Glass Compartment Series": [
            "9 compartment glass rack",
            "16 compartment glass rack",
            "25 compartment glass rack",
            "49 compartment glass rack"
        ]
    },

    # 4. TOTE BOXES
    "TOTE BOXES": {
        "Standard": [
            "600 x 400 x 370",
            "600 x 400 x 370 (A2b S.Printed)",
            "600 x 400 x 250",
            "400 x 300 x 300"
        ]
    },

    # 5. MS CONTAINERS
    "MS CONTAINERS": {
        "Standard": ["1100x800x690", "915x680x540"]
    },

    # 6. INSULATED BOXES
    "INSULATED BOXES": {
        "Red Ice Boxes (PVC)": {
            "SAF IR Series": ["25L", "35L", "50L", "60L", "100L", "150L"],
            "SAF IRCO Series": ["50L", "60L", "100L", "125L", "150L", "220L"],
            "SAF IRBD Series": ["45L"]
        },
        "Blue Ice Boxes (PVC)": {
            "SAF IRE Series": ["15L", "25L", "55L", "65L", "85L", "100L", "150L"],
            "SAF IR Series": ["30L", "35L", "45L"],
            "SAF IRCO Series": ["200L"]
        },
        "Fisheries Boxes (HDPE)": {
            "SAF IRF Series": ["50L", "70L", "100L", "150L", "220L", "260L", "310L", "460L", "660L", "1000L", "1250L"]
        }
    },

    # 7. KITCHEN EQUIPMENT
    "KITCHEN EQUIPMENT": {
        "Adjustable Dish Cart": {
            "SAF-J Series": [
                "SAF-J-DISHCART (B) (1090x720x800mm)",
                "SAF-J-DISHCART (M) (930x720x800mm)",
                "SAF-J-DISHCART (L) (900x725x800mm)"
            ]
        },
        "Insulated Milk Can": ["5L", "10L", "20L"],
        "Baking Tray Alusteel": ["Half Size", "Full Size", "Quarter Size"]
    },

    # 8. ROAD BARRIER
    "ROAD BARRIER": {
        "LLDPE": ["ROAD BARRIERS (2X1m)"],
        "HDPE": ["CRASH ROAD BARRIERS"]
    },

    # 9. HOME DECOR
    "HOME DECOR": {
        "Metal Bins": ["Metal Waste Bin With Front Open (1100L)"],
        "Ice Caddies": ["SAF-C-110 (815x585x740mm)"]
    },

    # 10. OTHER PRODUCTS
    "PLASTIC WHEEL DUSTBIN": ["SAF IMW-120 (120L)", "SAF IMW-240 (240L)", "SAF IMW-360 (360L)"],
    "BEVERAGE DISPENSER": ["18L", "26L", "40L"],
    "PORTABLE TOILETS": ["PVC", "Steel"],
    "HAND PALLET TRUCK": ["SAF-HPT-550 (1150mm)", "SAF-HPT-685 (1200mm)"],
    "TRAFFIC CONE": {
        "HDPE": ["750mm"],
        "LLDPE": ["1000mm"]
    },
    "HOSPITAL DUSTBIN": ["SAF-PD 10 (10L)", "SAF-PD 15 (15L)", "SAF-PD 30 (30L)", "SAF-PD 60 (60L)"],
    "CHEMICAL STORAGE TANKS": ["Perforated Pallet Box Container (HDPE)"],
    "STRETCH FILM DISPENSER": ["SAF-J-PWD", "SAF-J-PWD2"],
    "DISPLAY PALLET": ["EN2-0806 (800x600x130mm)", "EN2-1006 (1000x600x130mm)", "EN2-1206 (1200x600x130mm)"]
}

# --- Initialize Excel File if Not Exists ---
if not os.path.exists(FILE_NAME):
    current_year = datetime.now().year
    current_month = datetime.now().month
    days_in_month = get_days_in_month(current_year, current_month)
    
    columns = [
        "S.NO", "PRODUCT TYPE", "CATEGORY", "SUBCATEGORY", "PRODUCT",
        "DIMENSION", "CAPACITY", "COLOUR", "QTY", "STOCK PLACE",
        "REMARKS", "OPENING STOCK", "INWARD", "OUTWARD", "CLOSING STOCK"
    ]
    
    # Add columns for daily stock movement and closing stock
    for day in range(1, days_in_month + 1):
        date = f"{current_year}-{current_month:02d}-{day:02d}"
        columns.append(f"movement_{date}")
        columns.append(f"closing_{date}")
    
    pd.DataFrame(columns=columns).to_excel(FILE_NAME, sheet_name=SHEET_NAME, index=False)

# --- Load Data ---
df = pd.read_excel(FILE_NAME, sheet_name=SHEET_NAME)

# --- Streamlit App ---
st.title("\U0001F3ED SAF Products Stock Management")

# --- Date Selection ---
col_year, col_month = st.columns(2)
with col_year:
    selected_year = st.selectbox("Select Year", range(2024, 2031))
with col_month:
    months = list(calendar.month_name)[1:]
    selected_month = st.selectbox("Select Month", months)
selected_month_num = list(calendar.month_name).index(selected_month)

# --- Product Selection ---
product_type = st.selectbox("📦 SELECT PRODUCT TYPE", sorted(list(product_data.keys())))

if product_type not in product_data:
    st.error(f"❌ '{product_type}' not found in product_data.")
    st.stop()

# Selection Logic
category = ""
subcategory = ""
product_name = ""
dimension = ""
capacity = ""

selection = product_data[product_type]

if isinstance(selection, dict):
    categories = list(selection.keys())
    category = st.selectbox("🏷️ SELECT CATEGORY", categories)
    
    if isinstance(selection[category], dict):
        subcategories = list(selection[category].keys())
        subcategory = st.selectbox("📂 SELECT SUBCATEGORY", subcategories)
        products = selection[category][subcategory]
    else:
        products = selection[category]
else:
    products = selection

product = st.selectbox("🧾 SELECT PRODUCT", products)

# Parse product details
if "(" in product and ")" in product:
    product_name = product.split("(")[0].strip()
    specs = product.split("(")[1].split(")")[0]
    
    if "x" in specs or "mm" in specs or "m" in specs:
        dimension = specs
    elif "L" in specs or "l" in specs:
        capacity = specs
    elif "Kg" in specs:
        capacity = specs
else:
    product_name = product

# --- Stock Entry Form ---
with st.form("stock_form"):
    col1, col2 = st.columns(2)
    with col1:
        sno = st.number_input("S.NO", min_value=1)
        colour = st.text_input("COLOUR")
        qty = st.number_input("QUANTITY", min_value=0)
    with col2:
        location = st.text_input("STOCK LOCATION")
        remarks = st.text_input("REMARKS")
        opening = st.number_input("OPENING STOCK", min_value=0)

    inward = st.number_input("INWARD", min_value=0)
    outward = st.number_input("OUTWARD", min_value=0)
    closing = calculate_closing_stock(opening, inward, outward)
    st.write(f"Total Closing Stock: {closing}")

    st.subheader("🗓️ Daily Stock Movement")
    
    # Create calendar layout
    daily_data = {}
    daily_closing_stock = {}
    
    # Month header
    st.write(f"{selected_month} {selected_year}")
    
    # Calendar headers
    week_days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    cols_header = st.columns(7)
    for i, col in enumerate(cols_header):
        with col:
            st.markdown(f"**{week_days[i]}**")
    
    # Calendar days
    days_in_month = get_days_in_month(selected_year, selected_month_num)
    first_day_of_month = get_first_day_of_month(selected_year, selected_month_num)
    
    # Previous day's closing stock starts with opening stock
    prev_closing = opening

    # Create calendar grid
    day = 1
    for week in range(6):  # Maximum 6 weeks in a month
        cols = st.columns(7)
        for i in range(7):
            with cols[i]:
                if (week == 0 and i < first_day_of_month) or (day > days_in_month):
                    st.write("")  # Empty space
                else:
                    date = f"{selected_year}-{selected_month_num:02d}-{day:02d}"
                    
                    # Day container
                    st.markdown(f"**{day}**")
                    
                    # Stock movement input
                    movement = st.number_input(
                        "Movement",
                        key=f"movement_{date}",
                        help=f"+ for inward, - for outward"
                    )
                    daily_data[f"movement_{date}"] = movement
                    
                    # Calculate and display closing stock
                    daily_closing = prev_closing + movement
                    daily_closing_stock[f"closing_{date}"] = daily_closing
                    st.markdown(f"Closing: **{daily_closing}**")
                    
                    prev_closing = daily_closing
                    day += 1

    if st.form_submit_button("💾 SAVE ENTRY"):
        new_entry = {
            "S.NO": sno,
            "PRODUCT TYPE": product_type,
            "CATEGORY": category,
            "SUBCATEGORY": subcategory,
            "PRODUCT": product_name,
            "DIMENSION": dimension,
            "CAPACITY": capacity,
            "COLOUR": colour,
            "QTY": qty,
            "STOCK PLACE": location,
            "REMARKS": remarks,
            "OPENING STOCK": opening,
            "INWARD": inward,
            "OUTWARD": outward,
            "CLOSING STOCK": closing,
            **daily_data,
            **daily_closing_stock
        }

        # Ensure all columns exist
        for key in daily_data.keys():
            if key not in df.columns:
                df[key] = None
        for key in daily_closing_stock.keys():
            if key not in df.columns:
                df[key] = None

        if sno in df["S.NO"].values:
            idx = df[df["S.NO"] == sno].index[0]
            df.loc[idx] = new_entry
            st.success("Entry updated successfully! 🎉")
        else:
            df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
            st.success("New entry added successfully! 🎉")

        df.to_excel(FILE_NAME, sheet_name=SHEET_NAME, index=False)

# --- Download Data ---
st.subheader("📊 Download Data")
excel_data = BytesIO()
with pd.ExcelWriter(excel_data, engine='xlsxwriter') as writer:
    df.to_excel(writer, sheet_name=SHEET_NAME, index=False)
st.download_button(
    label="⬇️ Download Excel Report",
    data=excel_data.getvalue(),
    file_name=f"saf_stock_report_{selected_month}_{selected_year}.xlsx",
    mime="application/vnd.ms-excel"
)

# --- Preview Data ---
st.subheader("📋 Current Stock Data")
st.dataframe(df.head(10))

# Add filters for viewing data
st.subheader("🔍 Filter Data")
filter_col1, filter_col2 = st.columns(2)
with filter_col1:
    filter_product_type = st.selectbox("Filter by Product Type", ["All"] + sorted(list(product_data.keys())))
with filter_col2:
    filter_month = st.selectbox("Filter by Month", ["All"] + months)

# Apply filters
filtered_df = df.copy()
if filter_product_type != "All":
    filtered_df = filtered_df[filtered_df["PRODUCT TYPE"] == filter_product_type]
if filter_month != "All":
    month_num = list(calendar.month_name).index(filter_month)
    filtered_df = filtered_df[filtered_df.filter(like=f"-{month_num:02d}-").any(axis=1)]

if not filtered_df.empty:
    st.dataframe(filtered_df)
else:
    st.write("No data matches the selected filters.")

