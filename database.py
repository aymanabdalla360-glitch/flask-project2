# ==========================================
# استيراد مكتبة SQLite
# ==========================================

import sqlite3


# ==========================================
# اسم قاعدة البيانات
# ==========================================

DATABASE = "students.db"


# ==========================================
# إنشاء جدول الطلاب
# ==========================================

def create_table():

    # الاتصال بقاعدة البيانات
    conn = sqlite3.connect(DATABASE)

    # إنشاء الجدول إذا لم يكن موجودًا
    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            class_name TEXT NOT NULL,

            specialization TEXT NOT NULL,

            phone TEXT NOT NULL,

            address TEXT NOT NULL

        )
    """)

    # حفظ التغييرات
    conn.commit()

    # إغلاق الاتصال
    conn.close()


# ==========================================
# إضافة طالب جديد
# ==========================================

def add_student(
    name,
    class_name,
    specialization,
    phone,
    address
):

    # فتح الاتصال بقاعدة البيانات
    conn = sqlite3.connect(DATABASE)

    # إضافة بيانات الطالب
    conn.execute("""
        INSERT INTO students
        (
            name,
            class_name,
            specialization,
            phone,
            address
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        name,
        class_name,
        specialization,
        phone,
        address
    ))

    # حفظ البيانات
    conn.commit()

    # إغلاق الاتصال
    conn.close()


# ==========================================
# جلب جميع الطلاب
# ==========================================

def get_all_students():

    # فتح الاتصال
    conn = sqlite3.connect(DATABASE)

    # جلب جميع الطلاب
    cursor = conn.execute("""
        SELECT
            id,
            name,
            class_name,
            specialization,
            phone,
            address
        FROM students
    """)

    # الحصول على النتائج
    students = cursor.fetchall()

    # إغلاق الاتصال
    conn.close()

    # إعادة النتائج
    return students


# ==========================================
# جلب طالب واحد باستخدام ID
# ==========================================

def get_student(student_id):

    # فتح الاتصال
    conn = sqlite3.connect(DATABASE)

    # البحث عن الطالب
    cursor = conn.execute("""
        SELECT
            id,
            name,
            class_name,
            specialization,
            phone,
            address
        FROM students
        WHERE id = ?
    """, (student_id,))

    # الحصول على الطالب
    student = cursor.fetchone()

    # إغلاق الاتصال
    conn.close()

    # إعادة بيانات الطالب
    return student


# ==========================================
# تعديل بيانات طالب
# ==========================================

def update_student(
    student_id,
    name,
    class_name,
    specialization,
    phone,
    address
):

    # فتح الاتصال
    conn = sqlite3.connect(DATABASE)

    # تحديث بيانات الطالب
    conn.execute("""
        UPDATE students

        SET
            name = ?,
            class_name = ?,
            specialization = ?,
            phone = ?,
            address = ?

        WHERE id = ?
    """, (
        name,
        class_name,
        specialization,
        phone,
        address,
        student_id
    ))

    # حفظ التعديل
    conn.commit()

    # إغلاق الاتصال
    conn.close()


# ==========================================
# حذف طالب
# ==========================================

def delete_student(student_id):

    # فتح الاتصال
    conn = sqlite3.connect(DATABASE)

    # حذف الطالب
    conn.execute("""
        DELETE FROM students
        WHERE id = ?
    """, (student_id,))

    # حفظ الحذف
    conn.commit()

    # إغلاق الاتصال
    conn.close()


# ==========================================
# البحث عن الطلاب
# ==========================================

def search_students(search_text):

    # فتح الاتصال
    conn = sqlite3.connect(DATABASE)

    # البحث في الاسم أو الفصل أو التخصص
    cursor = conn.execute("""
        SELECT
            id,
            name,
            class_name,
            specialization,
            phone,
            address
        FROM students

        WHERE
            name LIKE ?
            OR class_name LIKE ?
            OR specialization LIKE ?
    """, (
        f"%{search_text}%",
        f"%{search_text}%",
        f"%{search_text}%"
    ))

    # الحصول على نتائج البحث
    students = cursor.fetchall()

    # إغلاق الاتصال
    conn.close()

    # إعادة النتائج
    return students