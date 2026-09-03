# ==========================================
# استيراد المكتبات
# ==========================================

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    flash
)


# ==========================================
# استيراد دوال قاعدة البيانات
# ==========================================

from database import (
    create_table,
    add_student,
    get_all_students,
    get_student,
    update_student,
    delete_student,
    search_students,
)


# ==========================================
# إنشاء تطبيق Flask
# ==========================================

app = Flask(__name__)


# ==========================================
# مفتاح سري لاستخدام رسائل flash
# ==========================================

app.secret_key = "student-management-secret"


# ==========================================
# إنشاء جدول الطلاب
# إذا لم يكن موجودًا
# ==========================================

create_table()


# ==========================================
# الصفحة الرئيسية
# ==========================================

@app.route("/")
def home():

    # جلب جميع الطلاب من قاعدة البيانات
    students = get_all_students()

    # حساب عدد الطلاب
    students_count = len(students)

    # إرسال عدد الطلاب إلى index.html
    return render_template(
        "index.html",
        students_count=students_count
    )


# ==========================================
# صفحة إضافة طالب
# ==========================================

@app.route("/form")
def form():

    # عرض نموذج إضافة الطالب
    return render_template("form.html")


# ==========================================
# استقبال بيانات الطالب
# ==========================================

@app.route("/submit", methods=["POST"])
def submit():

    # استقبال بيانات الطالب من النموذج
    name = request.form.get("name")
    class_name = request.form.get("class_name")
    specialization = request.form.get("specialization")
    phone = request.form.get("phone")
    address = request.form.get("address")


    # ==========================================
    # التأكد من إدخال جميع البيانات
    # ==========================================

    if not name or not class_name or not specialization or not phone or not address:

        return render_template(
            "form.html",
            error="من فضلك أدخل جميع بيانات الطالب"
        )


    # ==========================================
    # إضافة الطالب إلى قاعدة البيانات
    # ==========================================

    add_student(
        name,
        class_name,
        specialization,
        phone,
        address
    )


    # ==========================================
    # إرسال رسالة نجاح
    # ==========================================

    flash(
        "تمت إضافة الطالب بنجاح",
        "success"
    )


    # ==========================================
    # الانتقال إلى قائمة الطلاب
    # ==========================================

    return redirect("/students")


# ==========================================
# قائمة الطلاب
# ==========================================

@app.route("/students")
def students():

    # جلب جميع الطلاب من قاعدة البيانات
    students = get_all_students()

    # إرسال الطلاب إلى students.html
    return render_template(
        "students.html",
        students=students
    )


# ==========================================
# صفحة تعديل بيانات الطالب
# ==========================================

@app.route("/edit/<int:id>")
def edit(id):

    # جلب الطالب باستخدام ID
    student = get_student(id)


    # ==========================================
    # إذا لم نجد الطالب
    # ==========================================

    if student is None:

        return "الطالب غير موجود"


    # ==========================================
    # فتح صفحة التعديل
    # وإرسال بيانات الطالب
    # ==========================================

    return render_template(
        "edit.html",
        student=student
    )


# ==========================================
# استقبال بيانات التعديل
# ==========================================

@app.route("/update/<int:id>", methods=["POST"])
def update(id):

    # استقبال بيانات الطالب
    name = request.form.get("name")
    class_name = request.form.get("class_name")
    specialization = request.form.get("specialization")
    phone = request.form.get("phone")
    address = request.form.get("address")


    # ==========================================
    # التأكد من إدخال جميع البيانات
    # ==========================================

    if not name or not class_name or not specialization or not phone or not address:

        # جلب بيانات الطالب
        student = get_student(id)

        return render_template(
            "edit.html",
            student=student,
            error="من فضلك أدخل جميع بيانات الطالب"
        )


    # ==========================================
    # تحديث بيانات الطالب
    # ==========================================

    update_student(
        id,
        name,
        class_name,
        specialization,
        phone,
        address
    )


    # ==========================================
    # إرسال رسالة نجاح
    # ==========================================

    flash(
        "تم تعديل بيانات الطالب بنجاح",
        "success"
    )


    # ==========================================
    # العودة إلى قائمة الطلاب
    # ==========================================

    return redirect("/students")


# ==========================================
# حذف طالب
# ==========================================

@app.route("/delete/<int:id>")
def delete(id):

    # حذف الطالب من قاعدة البيانات
    delete_student(id)


    # ==========================================
    # إرسال رسالة نجاح
    # ==========================================

    flash(
        "تم حذف الطالب بنجاح",
        "success"
    )


    # ==========================================
    # العودة إلى قائمة الطلاب
    # ==========================================

    return redirect("/students")


# ==========================================
# البحث عن الطلاب
# ==========================================

@app.route("/search")
def search():

    # الحصول على كلمة البحث من الرابط
    search_text = request.args.get("search", "")


    # ==========================================
    # تنفيذ البحث في قاعدة البيانات
    # ==========================================

    students = search_students(search_text)


    # ==========================================
    # عرض نتائج البحث
    # ==========================================

    return render_template(
        "students.html",
        students=students
    )


# ==========================================
# تشغيل التطبيق
# ==========================================

if __name__ == "__main__":

    # تشغيل Flask في وضع Debug
    app.run(debug=True)