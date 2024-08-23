import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Initialize the Firebase app
cred = credentials.Certificate('mycart-93520-firebase-adminsdk-ws4ro-f943b7f8a5.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

data = {
  "products": [
    {
      "name": "Samsung Galaxy S23 Ultra 256GB",
      "category": "Electronics & Appliances",
      "product_id": "EA003",
      "price": 1100.00,
      "description": "High-end smartphone with advanced camera features and large storage capacity.",
      "quantity": 50,
      "image_url": "https://example.com/samsung_galaxy_s23.jpg",
      "brand": "Samsung",
      "offer": 10
    },
    {
        "name": "LG 55 Inch 4K UHD Smart TV",
        "category": "Electronics & Appliances",
        "product_id": "EA004",
        "price": 650.00,
        "description": "Ultra HD smart TV with vibrant picture quality and streaming apps.",
        "quantity": 40,
        "image_url": "https://example.com/lg_4k_tv.jpg",
        "brand": "LG",
        "offer": 5
    },
    {
        "name": "Nike Air Max 270",
        "category": "Apparel & Accessories",
        "product_id": "AA002",
        "price": 150.00,
        "description": "Popular Nike sneakers known for comfort and style.",
        "quantity": 70,
        "image_url": "https://example.com/nike_air_max_270.jpg",
        "brand": "Nike",
        "offer": 25
    },
    {
        "name": "Dyson V11 Cordless Vacuum Cleaner",
        "category": "Cleaning & Household",
        "product_id": "CH002",
        "price": 400.00,
        "description": "Powerful cordless vacuum with advanced filtration system.",
        "quantity": 30,
        "image_url": "https://example.com/dyson_v11.jpg",
        "brand": "Dyson",
        "offer": 0
    },
    {
        "name": "Adidas Ultraboost 22 Running Shoes",
        "category": "Apparel & Accessories",
        "product_id": "AA003",
        "price": 180.00,
        "description": "High-performance running shoes with responsive cushioning.",
        "quantity": 60,
        "image_url": "https://example.com/adidas_ultraboost_22.jpg",
        "brand": "Adidas",
        "offer": 0
    },
    {
        "name": "Tefal Cookware Set 10 Pieces",
        "category": "Home & Living",
        "product_id": "HL002",
        "price": 100.00,
        "description": "Non-stick cookware set including frying pans and saucepans.",
        "quantity": 50,
        "image_url": "https://example.com/tefal_cookware.jpg",
        "brand": "Tefal",
        "offer": 0
    },
    {
        "name": "Apple MacBook Pro 14 Inch 512GB",
        "category": "Electronics & Appliances",
        "product_id": "EA005",
        "price": 2000.00,
        "description": "Powerful laptop with M1 chip for professional use.",
        "quantity": 20,
        "image_url": "https://example.com/macbook_pro.jpg",
        "brand": "Apple",
        "offer": 0
    },
    {
        "name": "Pampers Baby-Dry Diapers Size 4",
        "category": "Baby & Kids",
        "product_id": "BK002",
        "price": 35.00,
        "description": "Super absorbent diapers for babies, size 4.",
        "quantity": 100,
        "image_url": "https://example.com/pampers_size4.jpg",
        "brand": "Pampers",
        "offer": 0
    },
    {
        "name": "Nutella Hazelnut Spread 750g",
        "category": "Food & Beverages",
        "product_id": "FB003",
        "price": 8.50,
        "description": "Popular chocolate hazelnut spread, 750g jar.",
        "quantity": 200,
        "image_url": "https://example.com/nutella_750g.jpg",
        "brand": "Nutella",
        "offer": 0
    },
    {
        "name": "Whiskas Dry Cat Food 1.5kg",
        "category": "Pet Supplies",
        "product_id": "PS002",
        "price": 15.00,
        "description": "Complete nutrition for adult cats, 1.5kg bag.",
        "quantity": 80,
        "image_url": "https://example.com/whiskas_cat_food.jpg",
        "brand": "Whiskas",
        "offer": 0
    },
    {
        "name": "Sony PlayStation 5",
        "category": "Toys & Hobbies",
        "product_id": "TH002",
        "price": 600.00,
        "description": "Next-gen gaming console with immersive graphics.",
        "quantity": 30,
        "image_url": "https://example.com/ps5.jpg",
        "brand": "Sony",
        "offer": 25
    },
    {
        "name": "Oral-B Electric Toothbrush Pro 2000",
        "category": "Health & Personal Care",
        "product_id": "HPC002",
        "price": 70.00,
        "description": "Advanced electric toothbrush with pressure sensor.",
        "quantity": 100,
        "image_url": "https://example.com/oral_b_pro_2000.jpg",
        "brand": "Oral-B",
        "offer": 0
    },
    {
        "name": "Levi's 501 Original Fit Jeans",
        "category": "Apparel & Accessories",
        "product_id": "AA004",
        "price": 85.00,
        "description": "Classic straight-leg jeans from Levi's.",
        "quantity": 50,
        "image_url": "https://example.com/levis_501.jpg",
        "brand": "Levi's",
        "offer": 0
    },
    {
        "name": "Nescafe Gold Blend Coffee 200g",
        "category": "Food & Beverages",
        "product_id": "FB004",
        "price": 6.00,
        "description": "Premium instant coffee with rich flavor.",
        "quantity": 150,
        "image_url": "https://example.com/nescafe_gold.jpg",
        "brand": "Nescafe",
        "offer": 0
    },
    {
        "name": "Bosch Front Load Washing Machine 8kg",
        "category": "Electronics & Appliances",
        "product_id": "EA006",
        "price": 500.00,
        "description": "Efficient front-load washing machine with multiple wash programs.",
        "quantity": 25,
        "image_url": "https://example.com/bosch_washing_machine.jpg",
        "brand": "Bosch",
        "offer": 0
    },
    {
        "name": "Maybelline SuperStay Matte Ink Lipstick",
        "category": "Health & Beauty",
        "product_id": "HB002",
        "price": 12.00,
        "description": "Long-lasting liquid lipstick with a matte finish.",
        "quantity": 100,
        "image_url": "https://example.com/maybelline_matte_ink.jpg",
        "brand": "Maybelline",
        "offer": 0
    },
    {
        "name": "HP DeskJet 2720 All-in-One Printer",
        "category": "Electronics & Appliances",
        "product_id": "EA007",
        "price": 65.00,
        "description": "Compact all-in-one printer for home use.",
        "quantity": 40,
        "image_url": "https://example.com/hp_deskjet_2720.jpg",
        "brand": "HP",
        "offer": 0
    },
    {
        "name": "L'Oreal Paris Revitalift Cream 50ml",
        "category": "Health & Beauty",
        "product_id": "HB003",
        "price": 25.00,
        "description": "Anti-aging face cream with Pro-Retinol.",
        "quantity": 80,
        "image_url": "https://example.com/loreal_revitalift.jpg",
        "brand": "L'Oreal Paris",
        "offer": 0
    },
    {
        "name": "Huawei Watch GT 3 Pro",
        "category": "Electronics & Appliances",
        "product_id": "EA008",
        "price": 300.00,
        "description": "Elegant smartwatch with advanced health monitoring and long battery life.",
        "quantity": 45,
        "image_url": "https://example.com/huawei_watch_gt3.jpg",
        "brand": "Huawei",
        "offer": 0
    },
    {
        "name": "IKEA Malm 4-Drawer Chest",
        "category": "Home & Living",
        "product_id": "HL003",
        "price": 120.00,
        "description": "Spacious chest of drawers with a clean design.",
        "quantity": 60,
        "image_url": "https://example.com/ikea_malm.jpg",
        "brand": "IKEA",
        "offer": 0
    },
    {
        "name": "Canon EOS 200D II DSLR Camera",
        "category": "Electronics & Appliances",
        "product_id": "EA009",
        "price": 550.00,
        "description": "Lightweight DSLR camera with a versatile lens kit for beginners.",
        "quantity": 30,
        "image_url": "https://example.com/canon_eos_200d.jpg",
        "brand": "Canon",
        "offer": 0
    },
    {
        "name": "Olay Total Effects 7-in-1 Day Cream",
        "category": "Health & Beauty",
        "product_id": "HB004",
        "price": 28.00,
        "description": "Anti-aging cream with SPF 15 to protect and nourish skin.",
        "quantity": 80,
        "image_url": "https://example.com/olay_total_effects.jpg",
        "brand": "Olay",
        "offer": 0
    },
    {
        "name": "Nestle NIDO Fortified Milk Powder 2.25kg",
        "category": "Food & Beverages",
        "product_id": "FB005",
        "price": 22.00,
        "description": "Fortified milk powder for children aged 1 and above.",
        "quantity": 150,
        "image_url": "https://example.com/nido_milk_powder.jpg",
        "brand": "Nestle",
        "offer": 0
    },
    {
        "name": "Black+Decker 18V Cordless Drill",
        "category": "Automotive & Tools",
        "product_id": "AT002",
        "price": 95.00,
        "description": "Versatile cordless drill with adjustable speed settings.",
        "quantity": 50,
        "image_url": "https://example.com/black_decker_drill.jpg",
        "brand": "Black+Decker",
        "offer": 0
    },
    {
        "name": "Philips Airfryer XXL",
        "category": "Electronics & Appliances",
        "product_id": "EA010",
        "price": 280.00,
        "description": "Large-capacity air fryer with rapid air technology for healthy cooking.",
        "quantity": 40,
        "image_url": "https://example.com/philips_airfryer.jpg",
        "brand": "Philips",
        "offer": 0
    },
    {
        "name": "Lenovo IdeaPad 3 Laptop 15.6\"",
        "category": "Electronics & Appliances",
        "product_id": "EA011",
        "price": 450.00,
        "description": "Affordable laptop with AMD Ryzen 5, 8GB RAM, and 256GB SSD.",
        "quantity": 60,
        "image_url": "https://example.com/lenovo_ideapad3.jpg",
        "brand": "Lenovo",
        "offer": 0
    },
    {
        "name": "Jordan 1 Retro High OG Sneakers",
        "category": "Apparel & Accessories",
        "product_id": "AA005",
        "price": 200.00,
        "description": "Iconic high-top sneakers from Nike's Air Jordan line.",
        "quantity": 50,
        "image_url": "https://example.com/jordan_1.jpg",
        "brand": "Nike",
        "offer": 0
    },
    {
        "name": "Dettol Antibacterial Surface Cleaner 1L",
        "category": "Cleaning & Household",
        "product_id": "CH003",
        "price": 5.00,
        "description": "Kills 99.9% of bacteria and viruses, leaving surfaces hygienic.",
        "quantity": 150,
        "image_url": "https://example.com/dettol_cleaner.jpg",
        "brand": "Dettol",
        "offer": 0
    },
    {
        "name": "Vaseline Intensive Care Aloe Soothe Lotion 400ml",
        "category": "Health & Beauty",
        "product_id": "HB005",
        "price": 6.00,
        "description": "Moisturizing lotion with aloe vera for dry skin.",
        "quantity": 100,
        "image_url": "https://example.com/vaseline_aloe_lotion.jpg",
        "brand": "Vaseline",
        "offer": 0
    },
    {
        "name": "ASICS Gel-Kayano 28 Running Shoes",
        "category": "Apparel & Accessories",
        "product_id": "AA006",
        "price": 160.00,
        "description": "Stability running shoes with excellent cushioning.",
        "quantity": 60,
        "image_url": "https://example.com/asics_gel_kayano.jpg",
        "brand": "ASICS",
        "offer": 0
    },
    {
        "name": "JBL Flip 5 Bluetooth Speaker",
        "category": "Electronics & Appliances",
        "product_id": "EA012",
        "price": 95.00,
        "description": "Portable waterproof Bluetooth speaker with powerful sound.",
        "quantity": 80,
        "image_url": "https://example.com/jbl_flip5.jpg",
        "brand": "JBL",
        "offer": 0
    },
    {
        "name": "Tommy Hilfiger Men's Casual Shirt",
        "category": "Apparel & Accessories",
        "product_id": "AA007",
        "price": 70.00,
        "description": "Stylish casual shirt perfect for everyday wear.",
        "quantity": 50,
        "image_url": "https://example.com/tommy_shirt.jpg",
        "brand": "Tommy Hilfiger",
        "offer": 0
    },
    {
        "name": "Sony WH-1000XM4 Noise Cancelling Headphones",
        "category": "Electronics & Appliances",
        "product_id": "EA013",
        "price": 350.00,
        "description": "Premium noise-cancelling headphones with superior sound quality.",
        "quantity": 40,
        "image_url": "https://example.com/sony_wh1000xm4.jpg",
        "brand": "Sony",
        "offer": 0
    },
    {
        "name": "Persil Bio Liquid Detergent 2.5L",
        "category": "Cleaning & Household",
        "product_id": "CH004",
        "price": 9.00,
        "description": "Effective liquid detergent for all types of laundry.",
        "quantity": 120,
        "image_url": "https://example.com/persil_bio.jpg",
        "brand": "Persil",
        "offer": 0
    },
    {
        "name": "Apple iPad 10.2\" 9th Gen 64GB",
        "category": "Electronics & Appliances",
        "product_id": "EA014",
        "price": 330.00,
        "description": "Versatile tablet with a 10.2-inch Retina display.",
        "quantity": 50,
        "image_url": "https://example.com/ipad_102.jpg",
        "brand": "Apple",
        "offer": 0
    },
    {
        "name": "Lacoste Classic Polo Shirt",
        "category": "Apparel & Accessories",
        "product_id": "AA008",
        "price": 95.00,
        "description": "Iconic polo shirt with a comfortable fit.",
        "quantity": 60,
        "image_url": "https://example.com/lacoste_polo.jpg",
        "brand": "Lacoste",
        "offer": 0
    },
    {
        "name": "Samsung Galaxy Watch 4",
        "category": "Electronics & Appliances",
        "product_id": "EA015",
        "price": 270.00,
        "description": "Smartwatch with health monitoring and fitness tracking features.",
        "quantity": 50,
        "image_url": "https://example.com/galaxy_watch4.jpg",
        "brand": "Samsung",
        "offer": 20
    },
    {
        "name": "Kenwood Chef Titanium Mixer",
        "category": "Electronics & Appliances",
        "product_id": "EA016",
        "price": 450.00,
        "description": "High-performance stand mixer with multiple attachments for versatile cooking.",
        "quantity": 30,
        "image_url": "https://example.com/kenwood_mixer.jpg",
        "brand": "Kenwood",
        "offer": 0
    },
    {
        "name": "Clinique Moisture Surge 72-Hour Auto-Replenishing Hydrator",
        "category": "Health & Beauty",
        "product_id": "HB006",
        "price": 40.00,
        "description": "Lightweight gel-cream that provides up to 72 hours of hydration.",
        "quantity": 90,
        "image_url": "https://example.com/clinique_moisture_surge.jpg",
        "brand": "Clinique",
        "offer": 0
    },
    {
        "name": "Dyson Pure Cool Air Purifier and Fan",
        "category": "Electronics & Appliances",
        "product_id": "EA017",
        "price": 550.00,
        "description": "Air purifier and fan combo with advanced filtration and quiet operation.",
        "quantity": 25,
        "image_url": "https://example.com/dyson_pure_cool.jpg",
        "brand": "Dyson",
        "offer": 0
    },
    {
        "name": "Huggies Little Movers Diapers Size 5",
        "category": "Baby & Kids",
        "product_id": "BK003",
        "price": 40.00,
        "description": "Comfortable and absorbent diapers for active toddlers, size 5.",
        "quantity": 120,
        "image_url": "https://example.com/huggies_size5.jpg",
        "brand": "Huggies",
        "offer": 0
    },
    {
        "name": "Whirlpool 8kg Top Load Washing Machine",
        "category": "Electronics & Appliances",
        "product_id": "EA018",
        "price": 370.00,
        "description": "Top load washing machine with advanced wash options and energy efficiency.",
        "quantity": 40,
        "image_url": "https://example.com/whirlpool_top_load.jpg",
        "brand": "Whirlpool",
        "offer": 0
    },
    {
        "name": "Garnier Fructis Sleek & Shine Shampoo 370ml",
        "category": "Health & Beauty",
        "product_id": "HB007",
        "price": 8.00,
        "description": "Shampoo for frizzy hair with argan oil for smooth and shiny results.",
        "quantity": 150,
        "image_url": "https://example.com/garnier_sleek_shampoo.jpg",
        "brand": "Garnier",
        "offer": 0
    },
    {
        "name": "Nestle NAN Optipro 1 Infant Formula 800g",
        "category": "Baby & Kids",
        "product_id": "BK004",
        "price": 25.00,
        "description": "Infant formula with optimized protein blend for newborns.",
        "quantity": 100,
        "image_url": "https://example.com/nan_optipro1.jpg",
        "brand": "Nestle",
        "offer": 0
    },
    {
        "name": "Samsung 75\" QLED 4K Smart TV",
        "category": "Electronics & Appliances",
        "product_id": "EA019",
        "price": 1400.00,
        "description": "Large-screen QLED TV with 4K resolution and smart features.",
        "quantity": 20,
        "image_url": "https://example.com/samsung_qled_75.jpg",
        "brand": "Samsung",
        "offer": 0
    },
    {
        "name": "Bosch 18V Cordless Jigsaw",
        "category": "Automotive & Tools",
        "product_id": "AT003",
        "price": 120.00,
        "description": "Powerful cordless jigsaw with precision cutting for DIY projects.",
        "quantity": 30,
        "image_url": "https://example.com/bosch_jigsaw.jpg",
        "brand": "Bosch",
        "offer": 0
    },
    {
        "name": "L'Oreal Paris Voluminous Lash Paradise Mascara",
        "category": "Health & Beauty",
        "product_id": "HB008",
        "price": 14.00,
        "description": "Volumizing mascara that provides intense length and volume.",
        "quantity": 100,
        "image_url": "https://example.com/loreal_lash_paradise.jpg",
        "brand": "L'Oreal Paris",
        "offer": 0
    },
    {
        "name": "Sony Alpha A7 III Mirrorless Camera",
        "category": "Electronics & Appliances",
        "product_id": "EA020",
        "price": 1800.00,
        "description": "Full-frame mirrorless camera with exceptional image quality and fast autofocus.",
        "quantity": 15,
        "image_url": "https://example.com/sony_alpha_a7iii.jpg",
        "brand": "Sony",
        "offer": 10
    },
    {
        "name": "Pampers Aqua Pure Baby Wipes 48 Count",
        "category": "Baby & Kids",
        "product_id": "BK005",
        "price": 6.00,
        "description": "Hypoallergenic baby wipes made with 99% water.",
        "quantity": 150,
        "image_url": "https://example.com/pampers_aqua_pure.jpg",
        "brand": "Pampers",
        "offer": 0
    },
    {ds
        "name": "Braun Series 7 Electric Shaver",
        "category": "Health & Beauty",
        "product_id": "HB009",
        "price": 200.00,
        "description": "Smart electric shaver with adaptive shaving technology.",
        "quantity": 40,
        "image_url": "https://example.com/braun_series7.jpg",
        "brand": "Braun",
        "offer": 0
    },
    {
        "name": "HP 24\" Full HD Monitor",
        "category": "Electronics & Appliances",
        "product_id": "EA021",
        "price": 160.00,
        "description": "Full HD monitor with IPS technology for vibrant colors and wide viewing angles.",
        "quantity": 60,
        "image_url": "https://example.com/hp_24_monitor.jpg",
        "brand": "HP",
        "offer": 0
    },
    {
        "name": "Jordan 1 Mid SE Shoes",
        "category": "Apparel & Accessories",
        "product_id": "AA009",
        "price": 180.00,
        "description": "Stylish mid-top sneakers with a unique design.",
        "quantity": 50,
        "image_url": "https://example.com/jordan_1_mid_se.jpg",
        "brand": "Nike",
        "offer": 0
    },
    {
        "name": "Sony Bravia 55\" OLED 4K Ultra HD Smart TV",
        "category": "Electronics & Appliances",
        "product_id": "EA022",
        "price": 1200.00,
        "description": "OLED TV with stunning 4K resolution and vibrant colors.",
        "quantity": 30,
        "image_url": "https://example.com/sony_bravia_oled.jpg",
        "brand": "Sony",
        "offer": 0
    },
    {
        "name": "Himalaya Herbal Face Wash 150ml",
        "category": "Health & Beauty",
        "product_id": "HB010",
        "price": 5.00,
        "description": "Natural face wash with neem and turmeric for clear skin.",
        "quantity": 100,
        "image_url": "https://example.com/himalaya_face_wash.jpg",
        "brand": "Himalaya",
        "offer": 0
    },
    {
        "name": "Apple iMac 24\" M1 Chip 256GB",
        "category": "Electronics & Appliances",
        "product_id": "EA023",
        "price": 1700.00,
        "description": "All-in-one desktop computer",
        "quantity": 100,
        "image_url": "https://example.com/himalaya_face_wash.jpg",
        "brand": "Apple",
        "offer": 0
    }
   
      ]
      }


 #Reference to the Firestore collection
collection_ref = db.collection('products')

# Upload each product to Firestore
for product in data['products']:
    doc_id = product['product_id']
    collection_ref.document(doc_id).set(product)

print("Data uploaded successfully!")