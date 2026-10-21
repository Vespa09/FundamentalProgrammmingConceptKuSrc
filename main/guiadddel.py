import customtkinter as ctk
import data  # ดึงข้อมูลจาก data.py

# ตั้งค่าธีม CustomTkinter
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")


# ==============================================================================
# 1. PURE FUNCTIONS (ฟังก์ชันบริสุทธิ์: ไม่มี Side Effect / ไม่แตะ UI / ไม่เชื่อม DB)
# ==============================================================================

def generate_next_id(existing_ids: list[str], prefix: str) -> str:
    """
    [Pure Function] คำนวณรหัส ID ถัดไปจากรายการ ID ที่มีในระบบ
    Input: (['F1', 'F2', 'F3'], 'F') -> Output: 'F4'
    """
    numbers = []
    for item_id in existing_ids:
        if item_id and item_id.startswith(prefix):
            num_part = item_id[len(prefix):]
            if num_part.isdigit():
                numbers.append(int(num_part))
    
    next_num = max(numbers) + 1 if numbers else 1
    return f"{prefix}{next_num}"


def format_menu_info_text(item_id: str, name: str, price: float, desc: str = "") -> str:
    """
    [Pure Function] แปลงข้อมูลเมนูเป็น String สำหรับแสดงผลบน UI
    """
    text = f"[{item_id}]  {name}\nราคา: {price:.2f} บาท"
    if desc:
        text += f" ({desc})"
    return text


def validate_menu_input(name: str, price_str: str) -> tuple[bool, str, float]:
    """
    [Pure Function] ตรวจสอบความถูกต้องของชื่อและราคา
    Input: (name, price_str) -> Output: (ผ่านหรือไม่, ข้อความแจ้งเตือน, ราคาที่แปลงแล้ว)
    """
    clean_name = name.strip()
    clean_price = price_str.strip()

    if not clean_name or not clean_price:
        return False, "กรุณากรอกข้อมูล ชื่อ และราคา ให้ครบถ้วน", 0.0

    try:
        price = float(clean_price)
        if price < 0:
            return False, "ราคาต้องไม่ติดลบ", 0.0
        return True, "", price
    except ValueError:
        return False, "กรุณากรอกราคาเป็นตัวเลขให้ถูกต้อง", 0.0


def is_food_category(cat_str: str) -> bool:
    """
    [Pure Function] เช็กประเภทจากข้อความใน OptionMenu
    """
    return "Food" in cat_str or "อาหาร" in cat_str


# ==============================================================================
# 2. IMPURE / GUI FUNCTIONS (จัดการการแสดงผล, Dialog และการเรียกใช้ DB)
# ==============================================================================

def update_auto_id_display(cat_str: str, entry_id_widget: ctk.CTkEntry):
    """ดึง ID ล่าสุดจาก DB แล้วคำนวณ ID ถัดไปมาใส่ในช่อง Entry"""
    is_food = is_food_category(cat_str)
    existing_ids = data.get_all_menu_ids(is_food)
    prefix = "F" if is_food else "D"
    
    next_id = generate_next_id(existing_ids, prefix)
    
    entry_id_widget.configure(state="normal")
    entry_id_widget.delete(0, "end")
    entry_id_widget.insert(0, next_id)
    entry_id_widget.configure(state="disabled")  # ปิดไม่ให้ผู้ใช้แก้ไขรหัสเอง


def show_alert(parent, title: str, message: str, color: str = "#E74C3C"):
    """แสดง Pop-up แจ้งเตือน"""
    dialog = ctk.CTkToplevel(parent)
    dialog.title(title)
    dialog.geometry("320x150")
    dialog.grab_set()

    lbl = ctk.CTkLabel(dialog, text=message, text_color=color, font=("Arial", 13, "bold"), wraplength=280)
    lbl.pack(pady=25)

    btn = ctk.CTkButton(dialog, text="ตกลง", width=90, command=dialog.destroy)
    btn.pack(pady=5)


def reload_menu_list(container_frame: ctk.CTkScrollableFrame, category: str, parent_app):
    """โหลดและวาดรายการอาหาร/เครื่องดื่มใหม่ใน ScrollableFrame"""
    for widget in container_frame.winfo_children():
        widget.destroy()

    items = data.menu() if category == "food" else data.menu_drink()

    if not items:
        lbl_empty = ctk.CTkLabel(container_frame, text="ไม่มีรายการเมนูในระบบ", text_color="#8A8888")
        lbl_empty.pack(pady=20)
        return

    for item in items:
        item_id, name, price = item[0], item[1], item[2]
        desc = item[3] if len(item) > 3 and item[3] else ""

        card = ctk.CTkFrame(container_frame, fg_color="#2B2B2B", corner_radius=8)
        card.pack(fill="x", padx=5, pady=5)

        info_text = format_menu_info_text(item_id, name, price, desc)

        lbl_info = ctk.CTkLabel(card, text=info_text, anchor="w", font=("Arial", 13), justify="left")
        lbl_info.pack(side="left", padx=12, pady=10, expand=True, fill="x")

        btn_delete = ctk.CTkButton(
            card,
            text="🗑️ ลบ",
            fg_color="#D64545",
            hover_color="#B03A3A",
            width=70,
            height=32,
            command=lambda cat=category, i_id=item_id, i_name=name: confirm_delete_dialog(
                parent_app, cat, i_id, i_name, lambda: reload_menu_list(container_frame, cat, parent_app)
            )
        )
        btn_delete.pack(side="right", padx=10, pady=10)


def confirm_delete_dialog(parent_app, category: str, item_id: str, name: str, on_success_callback):
    """Pop-up ยืนยันการลบรายการ"""
    dialog = ctk.CTkToplevel(parent_app)
    dialog.title("ยืนยันการลบ")
    dialog.geometry("340x170")
    dialog.grab_set()

    lbl_msg = ctk.CTkLabel(
        dialog,
        text=f"คุณต้องการลบเมนูนี้ใช่หรือไม่?\n\n[{item_id}] {name}",
        font=("Arial", 13, "bold"),
        text_color="#FFFFFF"
    )
    lbl_msg.pack(pady=(20, 15))

    btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
    btn_frame.pack(pady=5)

    def on_confirm():
        success = data.delete_menu_item(item_id) if category == "food" else data.delete_drink_item(item_id)
        dialog.grab_release()
        dialog.destroy()

        if success:
            on_success_callback()
            show_alert(parent_app, "สำเร็จ", f"ลบเมนู [{item_id}] {name} เรียบร้อยแล้ว", "#00A86B")
        else:
            show_alert(parent_app, "ข้อผิดพลาด", "ไม่สามารถลบรายการได้", "#D64545")

    btn_yes = ctk.CTkButton(btn_frame, text="ลบรายการ", fg_color="#D64545", hover_color="#B03A3A", command=on_confirm, width=110)
    btn_no = ctk.CTkButton(btn_frame, text="ยกเลิก", fg_color="#555555", hover_color="#333333", command=dialog.destroy, width=110)

    btn_yes.pack(side="left", padx=8)
    btn_no.pack(side="right", padx=8)


def handle_add_menu(entries: dict, parent_app, reload_callbacks: dict):
    """จัดการอีเวนต์เมื่อกดปุ่มบันทึกเพิ่มเมนู"""
    cat_str = entries["option_cat"].get()
    item_id = entries["entry_id"].get()  # ID ที่ถูกสร้างอัตโนมัติ
    name = entries["entry_name"].get()
    price_str = entries["entry_price"].get()
    desc = entries["entry_desc"].get().strip()

    # 1. ตรวจสอบชื่อและราคาผ่าน Pure Function
    is_valid, err_msg, price = validate_menu_input(name, price_str)
    if not is_valid:
        show_alert(parent_app, "แจ้งเตือน", err_msg, "#D64545")
        return

    is_food = is_food_category(cat_str)
    category = "food" if is_food else "drink"

    # 2. บันทึกลง DB
    success = data.add_menu_item(item_id, name.strip(), price, desc) if is_food else data.add_drink_item(item_id, name.strip(), price, desc)

    if success:
        # ล้างข้อมูลในฟอร์ม (ยกเว้น ID ที่จะ Auto Refresh)
        entries["entry_name"].delete(0, "end")
        entries["entry_price"].delete(0, "end")
        entries["entry_desc"].delete(0, "end")

        # Reload รายการในแท็บ และอัปเดต Auto ID ถัดไป
        reload_callbacks[category]()
        update_auto_id_display(cat_str, entries["entry_id"])

        show_alert(parent_app, "สำเร็จ", f"เพิ่มเมนู [{item_id}] {name} เรียบร้อยแล้ว", "#00A86B")
    else:
        show_alert(parent_app, "ข้อผิดพลาด", "ไม่สามารถเพิ่มเมนูได้", "#D64545")


# ==============================================================================
# 3. MAIN APPLICATION ENTRY POINT (การประกอบ UI)
# ==============================================================================

def create_app():
    app = ctk.CTk()
    app.title("PyRestaurant - ระบบจัดการเมนูอาหาร (Admin)")
    app.geometry("580x680")
    app.resizable(False, False)

    lbl_title = ctk.CTkLabel(
        app,
        text="🍱 จัดการเมนูอาหาร & เครื่องดื่ม",
        font=("Arial", 20, "bold"),
        text_color="#00A86B"
    )
    lbl_title.pack(pady=(15, 10))

    tabview = ctk.CTkTabview(app, width=540, height=580)
    tabview.pack(padx=20, pady=(0, 20), fill="both", expand=True)

    tab_food = tabview.add("🍲 เมนูอาหาร")
    tab_drink = tabview.add("🥤 เครื่องดื่ม")
    tab_add = tabview.add("➕ เพิ่มเมนูใหม่")

    # Scrollable Frames สำหรับแสดงรายการ
    frame_food = ctk.CTkScrollableFrame(tab_food, width=500, height=480)
    frame_food.pack(fill="both", expand=True, padx=5, pady=5)

    frame_drink = ctk.CTkScrollableFrame(tab_drink, width=500, height=480)
    frame_drink.pack(fill="both", expand=True, padx=5, pady=5)

    # Dictionary เก็บ Callback สำหรับ Reload
    reload_callbacks = {
        "food": lambda: reload_menu_list(frame_food, "food", app),
        "drink": lambda: reload_menu_list(frame_drink, "drink", app)
    }

    # โหลดรายการเริ่มต้น
    reload_callbacks["food"]()
    reload_callbacks["drink"]()

    # --- สร้าง UI ใน Tab เพิ่มเมนู ---
    add_frame = ctk.CTkFrame(tab_add, fg_color="transparent")
    add_frame.pack(padx=20, pady=20, fill="both", expand=True)

    ctk.CTkLabel(add_frame, text="ประเภทเมนู:", font=("Arial", 13, "bold")).pack(anchor="w", pady=(5, 2))
    option_cat = ctk.CTkOptionMenu(
        add_frame, 
        values=["อาหาร (Food)", "เครื่องดื่ม (Drink)"],
        command=lambda selected_val: update_auto_id_display(selected_val, entry_id)
    )
    option_cat.pack(fill="x", pady=(0, 10))

    ctk.CTkLabel(add_frame, text="รหัสเมนู (Auto Generated):", font=("Arial", 13, "bold")).pack(anchor="w", pady=(5, 2))
    entry_id = ctk.CTkEntry(add_frame, fg_color="#333333", text_color="#00FF3C", font=("Arial", 13, "bold"))
    entry_id.pack(fill="x", pady=(0, 10))

    ctk.CTkLabel(add_frame, text="ชื่อเมนู:", font=("Arial", 13, "bold")).pack(anchor="w", pady=(5, 2))
    entry_name = ctk.CTkEntry(add_frame, placeholder_text="กรอกชื่ออาหาร/เครื่องดื่ม")
    entry_name.pack(fill="x", pady=(0, 10))

    ctk.CTkLabel(add_frame, text="ราคา (บาท):", font=("Arial", 13, "bold")).pack(anchor="w", pady=(5, 2))
    entry_price = ctk.CTkEntry(add_frame, placeholder_text="กรอกราคา เช่น 50")
    entry_price.pack(fill="x", pady=(0, 10))

    ctk.CTkLabel(add_frame, text="คำอธิบาย (Optional):", font=("Arial", 13, "bold")).pack(anchor="w", pady=(5, 2))
    entry_desc = ctk.CTkEntry(add_frame, placeholder_text="เช่น เผ็ดน้อย, หวานชื่นใจ")
    entry_desc.pack(fill="x", pady=(0, 15))

    entries = {
        "option_cat": option_cat,
        "entry_id": entry_id,
        "entry_name": entry_name,
        "entry_price": entry_price,
        "entry_desc": entry_desc
    }

    # สร้าง Auto ID ครั้งแรกเมื่อเปิดแอป
    update_auto_id_display(option_cat.get(), entry_id)

    btn_add = ctk.CTkButton(
        add_frame,
        text="➕ บันทึกเพิ่มเมนู",
        fg_color="#00A86B",
        hover_color="#008F5B",
        font=("Arial", 14, "bold"),
        height=40,
        command=lambda: handle_add_menu(entries, app, reload_callbacks)
    )
    btn_add.pack(fill="x", pady=10)

    return app


if __name__ == "__main__":
    app = create_app()
    app.mainloop()