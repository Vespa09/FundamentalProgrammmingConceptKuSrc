# 🍽️ PyRestaurant - Restaurant Reservation & Ordering System

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![GUI Framework](https://img.shields.io/badge/GUI-CustomTkinter-orange.svg)](https://github.com/TomSchimansky/CustomTkinter)
[![Database](https://img.shields.io/badge/Database-SQLite3-lightgrey.svg)](https://www.sqlite.org/)

**PyRestaurant** เป็นแอปพลิเคชันเดสก์ท็อปสำหรับการจัดการการจองโต๊ะและการสั่งอาหารในร้านอาหารแบบครบวงจร พัฒนาด้วยภาษา Python โดยใช้ **CustomTkinter** สำหรับการออกแบบอินเทอร์เฟซผู้ใช้ (GUI) ร่วมกับฐานข้อมูล **SQLite**[span_0](start_span)[span_0](end_span)[span_1](start_span)[span_1](end_span)

โปรเจกต์นี้เป็นส่วนหนึ่งของวิชา **Fundamental Programming Concept** มหาวิทยาลัยเกษตรศาสตร์ วิทยาเขตศรีราชา[span_2](start_span)[span_2](end_span)

---

## 📋 สารบัญ (Table of Contents)
- [ระบบการทำงานและฟีเจอร์หลัก](#-ระบบการทำงานและฟีเจอร์หลัก-key-features)
- [แผนภาพลำดับการทำงาน (System Flowchart)](#-แผนภาพลำดับการทำงาน-system-flowchart)
- [โครงสร้างซอร์สโค้ด (Project Structure)](#-โครงสร้างซอร์สโค้ด-project-structure)
- [โครงสร้างตารางฐานข้อมูล (Database Schema)](#-โครงสร้างตารางฐานข้อมูล-database-schema)
- [ข้อกำหนดและการติดตั้ง (Installation & Requirements)](#-ข้อกำหนดและการติดตั้ง-installation--requirements)
- [สมาชิกผู้จัดทำ (Authors)](#-สมาชิกผู้จัดทำ-authors)

---

## ✨ ระบบการทำงานและฟีเจอร์หลัก (Key Features)

### 🔐 1. ระบบยืนยันตัวตน (Authentication & Security)
* **Register / Login:** รองรับการสมัครสมาชิกและเข้าสู่ระบบด้วย Username/Password[span_3](start_span)[span_3](end_span)[span_4](start_span)[span_4](end_span)
* **Data Validation:** ตรวจสอบรหัสผ่านขั้นต่ำ 6 ตัวอักษร[span_5](start_span)[span_5](end_span), รูปแบบเบอร์โทรศัพท์ และรูปแบบอีเมล[span_6](start_span)[span_6](end_span)
* **Duplicate Checking:** ตรวจสอบ Username, Phone และ Email ซ้ำในระบบ SQLite[span_7](start_span)[span_7](end_span)
* **Security Protection:** บล็อกการ Copy/Cut และคลิกขวาในช่องกรอกรหัสผ่านเพื่อป้องกันข้อมูลรั่วไหล[span_8](start_span)[span_8](end_span)

### 📅 2. ระบบจองโต๊ะอาหาร (Table Booking)
* **Table Availability Filter:** ค้นหาและกรองโต๊ะว่างตามวันที่ และช่วงเวลา[span_9](start_span)[span_9](end_span)
* **Auto Time Calculation:** คำนวณเวลาสิ้นสุดการจองให้อัตโนมัติ (+1 ชั่วโมง)[span_10](start_span)[span_10](end_span)
* **Booking Validation:** ป้องกันการเลือกเวลาสิ้นสุดก่อนเวลาเริ่มต้น และบล็อกการจองเวลาย้อนหลัง[span_11](start_span)[span_11](end_span)
* **Conflict Prevention:** ตรวจสอบสถานะการจองซ้ำในฐานข้อมูลตาราง `reservations` ก่อนบันทึกจริง[span_12](start_span)[span_12](end_span)

### 🍕 3. ระบบสั่งอาหารและจัดการตะกร้า (Ordering & Cart System)
* **Dynamic Menu Listing:** ดึงเมนูอาหารและเครื่องดื่มจาก SQLite มาแสดงผลพร้อมราคาสินค้า[span_13](start_span)[span_13](end_span)[span_14](start_span)[span_14](end_span)
* **Quantity Adjustment:** ปุ่มปรับเพิ่ม (+) และลด (-) จำนวนรายการอาหารบนหน้าจอ[span_15](start_span)[span_15](end_span)
* **Single Source of Truth Mapping:** ซิงค์รายการจองของผู้ใช้เพื่อระบุโต๊ะและรอบเวลาที่จะสั่งอาหารได้อย่างแม่นยำ[span_16](start_span)[span_16](end_span)[span_17](start_span)[span_17](end_span)
* **Real-time Cart Management:** คำนวณราคาสุทธิแบบเรียลไทม์ และเพิ่ม/ลดจำนวนสินค้าในตะกร้าได้อิสระ[span_18](start_span)[span_18](end_span)

### 💳 4. ระบบเช็กบิลและชำระเงิน (Check Bill & Payment)
* **Order Summary:** รวมกลุ่มออเดอร์ (`group_order`) เพื่อแสดงรายการอาหาร ยอดรวมรายเมนู และยอดรวมสุทธิ[span_19](start_span)[span_19](end_span)
* **Payment Channels:** รองรับตัวเลือกช่องทางการชำระเงิน (เงินสด, โอนเงิน, บัตรเครดิต)[span_20](start_span)[span_20](end_span)
* **Database Status Update:** อัปเดต `status_pay` เป็น `'จ่ายแล้ว'` ในตาราง `orders` เมื่อยืนยันการชำระเงิน[span_21](start_span)[span_21](end_span)

---

## 🔄 แผนภาพลำดับการทำงาน (System Flowchart)

```mermaid
flowchart TD
    Start([เริ่มต้นใช้งานโปรแกรม]) --> LoginCheck{เข้าสู่ระบบสำเร็จ ?}
    
    LoginCheck -- ไม่สำเร็จ / ยังไม่มีบัญชี --> RegisterPage[หน้าสมัครสมาชิก / Login]
    RegisterPage --> LoginCheck
    
    LoginCheck -- สำเร็จ --> MainMenu[หน้าเมนูหลัก Main Frame]
    
    MainMenu --> Choice{เลือกทำรายการ}
    
    Choice -- จองโต๊ะ --> BookingFrame[หน้า Booking Table]
    BookingFrame --> FilterTable[กรองวันที่ / เวลา / เลขโต๊ะ]
    FilterTable --> CheckBkStatus{โต๊ะว่างในเวลาดังกล่าว ?}
    CheckBkStatus -- ไม่ว่าง --> BookingFrame
    CheckBkStatus -- ว่าง --> ConfirmBk[ยืนยันการจองบันทึกลง reservations]
    ConfirmBk --> AskOrder{ต้องการสั่งอาหารต่อเลยหรือไม่ ?}
    AskOrder -- ใช่ --> OrderFrame
    AskOrder -- ไม่ --> MainMenu
    
    Choice -- สั่งอาหาร --> OrderFrame[หน้า Order List]
    OrderFrame --> SelectTable[เลือกโต๊ะที่จองไว้จาก Dropdown]
    SelectTable --> SelectMenu[เลือกรายการอาหาร/เครื่องดื่ม + ปรับจำนวน]
    SelectMenu --> ConfirmToCart[กด Confirm Order เข้าตะกร้าสินค้า]
    ConfirmToCart --> CartFrame[หน้า Cart]
    CartFrame --> ReviewCart{ตรวจสอบรายการในตะกร้า}
    ReviewCart -- ยืนยันการสั่ง --> SaveOrder[(บันทึกรายการลงตาราง orders\nstatus_pay = 'ยังไม่จ่าย')]
    SaveOrder --> MainMenu
    
    Choice -- เช็กบิล --> CheckBillFrame[หน้า Check Bill & Payment]
    CheckBillFrame --> LoadBill[(ดึงรายการออเดอร์ที่ค้างชำระ\nstatus_pay = 'ยังไม่จ่าย')]
    LoadBill --> ShowTotal[แสดงรายการอาหารและยอดรวมสุทธิ]
    ShowTotal --> SelectPayMethod[เลือกช่องทางชำระเงิน: เงินสด / โอน / บัตร]
    SelectPayMethod --> ConfirmPay[กด Confirm ยืนยันการชำระเงิน]
    ConfirmPay --> UpdateDB[(อัปเดตตาราง orders:\nstatus_pay = 'จ่ายแล้ว')]
    UpdateDB --> ClearBillUI[รีเซ็ตหน้าจอเช็กบิล ยอดเป็น 0.00 บาท]
    ClearBillUI --> MainMenu
    
    MainMenu --> Logout[กด Logout] --> Start

📂 โครงสร้างซอร์สโค้ด (Project Structure)
FundamentalProgrammmingConceptKuSrc/
├── database/
│   └── database.db          # SQLite Database File
├── main/
│   ├── gui.py               # Main UI Layout and Event Management (CustomTkinter)
│   ├── data.py              # SQLite Database Access Layer (CRUD Functions)
│   ├── order.py             # Business Logic for Order & Cart Operations
│   └── logic.py             # User Authentication Logic
└── README.md                # Project Documentation

🛢️ โครงสร้างตารางฐานข้อมูล (Database Schema)
 * User: เก็บข้อมูลผู้ใช้งาน (username, password, firstname, lastname, phone, email, role)
 * dining_tables: เก็บข้อมูลโต๊ะอาหาร (table_no, capacity, cost)
 * reservations: เก็บข้อมูลการจองโต๊ะ (id, table_no, customer, booking_date, time_slot, status)
 * menu_food & menu_drink: เก็บรายการเมนูอาหารและเครื่องดื่ม (id, food/drink, price, description)
 * orders: เก็บคำสั่งซื้อ (no_order, menu, quantity, totalprice, status, table_no, customer, day, time, status_pay)
⚙️ ข้อกำหนดและการติดตั้ง (Installation & Requirements)
Prerequisites
 * Python 3.10 ขึ้นไป
Installation Steps
 * Clone Repository:
   git clone [https://github.com/vespa/FundamentalProgrammmingConceptKuSrc.git](https://github.com/vespa/FundamentalProgrammmingConceptKuSrc.git)
cd FundamentalProgrammmingConceptKuSrc

 * Install Required Libraries:
   pip install customtkinter tkcalendar

 * Run Application:
   python main/gui.py

👥 สมาชิกผู้จัดทำ (Authors)
 * นาย ธนากร ขนทอง - รหัสนิสิต 6930200760
 * นาย แทนโชค สังข์วัย - รหัสนิสิต 6930200689
 * นางสาว กฤษยารัตน์ กลิ่นพิพัฒน์ - รหัสนิสิต 6930200018

