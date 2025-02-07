# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright 2025 ABDULLA BASHIR
#
##############################################################################
from datetime import datetime

import xlsxwriter
import base64
from odoo import fields, models, api, _


class wizard_contract_report(models.TransientModel):
    _name = 'wizard.contract.report'
    _description = 'Wizard Contract Report'

    xls_file = fields.Binary(string='Download')
    name = fields.Char(string='File name', size=64)
    state = fields.Selection([('choose', 'choose'),
                              ('download', 'download')], default="choose", string="Status")
    payslip_ids = fields.Many2many('res.partner', string="Contract Ref.",
                                   default=lambda self: self._context.get('active_ids'))

    def generate_lease_agreement(self):
        xls_filename = 'Lease_Agreement{}.xlsx'
        import xlsxwriter
        workbook = xlsxwriter.Workbook(xls_filename)
        worksheet = workbook.add_worksheet("Lease Agreement")

        # Define formats
        title_format = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter', 'font_size': 18})
        sub_title_format = workbook.add_format({'bold': True, 'align': 'left', 'valign': 'vcenter', 'font_size': 16})
        text_format = workbook.add_format({'align': 'left', 'valign': 'vcenter', 'font_size': 12})
        text_center_format = workbook.add_format({'align': 'center', 'valign': 'vcenter', 'font_size': 12})

        worksheet.set_column('A:Z', 30)

        # Title
        row = 0
        worksheet.merge_range(row, 0, row, 7,
                              "التألق للمقاولات والصيانة ذ.م.م\nAL TAALUQ CONTRACTING AND MAINTENANCE WLL\nعــــقــد إيـــجــار\nLease Agreement\n{AB17-2D}",
                              title_format)
        row += 2  # Leave a blank row

        # Date and Parties
        worksheet.write(row, 0, "إنه في تاريخ{ 17 أغسطس سنة 2022}  تم الاتفاق في الدوحة -قطر بين كل من:", text_format)
        worksheet.write(row, 6,
                        "This Lease Agreement (“Agreement”) is made in the Doha, State of Qatar as of the {17 of  August 2022} between:",
                        text_format)
        row += 2

        # First Party
        worksheet.write(row, 0, "السادة / التألق للمقاولات والصيانة ذ.م.م", text_format)
        worksheet.write(row, 6, "AL TAALUQ CONTRACTING AND MAINTENANCE WLL", text_format)
        row += 1

        worksheet.write(row, 0, "يسمى فيما بعد (الطرف الأول)", text_format)
        worksheet.write(row, 6, "(The First Party”)", text_format)
        row += 1

        worksheet.write(row, 0, "العنوان  : ص . ب 877       الدوحة – قطر", text_format)
        worksheet.write(row, 6, "with an address of:\nP.O.Box  877, Doha-Qatar,", text_format)
        row += 1

        worksheet.write(row, 0, "هاتف:   44477280،55501752", text_format)
        worksheet.write(row, 6, "Tel: 44477280, 55501752", text_format)
        row += 1

        worksheet.write(row, 0, "فاكس: 44478562", text_format)
        worksheet.write(row, 6, "Fax: 44478562", text_format)
        row += 1

        worksheet.write(row, 0, "رقم الاتصال بالصيانة : 33379725", text_format)
        worksheet.write(row, 6, "Maintenance Contact No: 33379725", text_format)
        row += 1

        worksheet.write(row, 0, "البريد الالكتروني: almahmoudtc@gmail.com", text_format)
        worksheet.write(row, 6, "Email: almahmoudtc@gmail.com", text_format)
        row += 2  # Leave a blank row

        worksheet.write(row, 0, "و", text_center_format)
        worksheet.write(row, 6, "And", text_center_format)
        row += 1

        # Second Party
        worksheet.write(row, 0, "السيد/ {بورجا اليزوندو}", text_format)
        worksheet.write(row, 6, "MR\Ms. {Javier Borja Elizondo}", text_format)
        row += 1

        worksheet.write(row, 0, "الرقم الشخصي: {28648400001}", text_format)
        worksheet.write(row, 6, "QID: {28648400001}", text_format)
        row += 1

        worksheet.write(row, 0, "يسمى فيما بعد (الطرف الثاني)", text_format)
        worksheet.write(row, 6, "(The Second Party”)", text_format)
        row += 1

        worksheet.write(row, 0, "العنوان : الدوحة-قطر ص.ب : {22550}", text_format)
        worksheet.write(row, 6, "P.O.BOX : {22550} Doha-Qatar", text_format)
        row += 1

        worksheet.write(row, 0, "هاتـف : 55386173/66603236", text_format)
        worksheet.write(row, 6, "Tel: 55386173, 66603236", text_format)
        row += 1

        worksheet.write(row, 0, "البريد الالكتروني : {j.borjae86@gmail.com}", text_format)
        worksheet.write(row, 6, "Email: {j.borjae86@gmail.com}", text_format)
        row += 2  # Leave a blank row

        # Premises
        worksheet.write(row, 0,
                        "لما كان الطرف الأول يملك حق تأجير {فيلا} رقم  (والكائنة {AB17-2D}) في منطقة {أبو هامور}.",
                        text_format)
        worksheet.write(row, 6, "WHEREAS the First Party has the right to lease his {Villa} No ({AB17-2D}) located in "
                                "{Abou Hamour} ) “The Leased Premises”).", text_format)
        row += 1

        worksheet.write(row, 0, "رقم الكهرباء : {1267434} رقم الماء: {1209307}", text_format)
        worksheet.write(row, 6, "Electricity No: {1267434} Water No: {1209307}", text_format)
        row += 2  # Leave a blank row

        worksheet.write(row, 0,
                        "وبما أن الطرف الثاني يرغب في إستئجار {الفيلا}  المذكور أعلاه ( العين المؤجرة ) فقد إتفق المتعاقدان بعد أن أقر كل منهما بأهليته القانونية للتعاقد وإبرام سائر التصرفات الأخرى على ما يلي :-",
                        text_format)
        worksheet.write(row, 6, "AND WHEREAS the Second Party is willing to rent the Leased {Villa}.", text_format)
        row += 1

        worksheet.write(row, 0,
                        "NOW THEREFORE, the Parties, after acknowledging their eligibility to enter into the Agreement and conclude all other acts, covenant and agree as follows:",
                        text_format)
        row += 2  # Leave a blank row

        # Agreement Points
        points = [
            ("1",
             "تعتبر المقدمة جزء لا يتجزأ من هذا العقد وتقرأ وتفسر معه كوحده واحده.",
             "The preamble is part and parcel of the Agreement, to be read and interpreted with it."),
            ("2",
             "مدة هذا العقد {(01) سنة}  تبدأ اعتباراً من   { 01 سبتمبر سنة 2022م} وتنتهي في {31 أغسطس سنة 2023م }ولا يحق لأي من الطرفين إنهاء هذا العقد قبل ذلك ، إلا حسب ما نص عليه هذا العقد ، وفي حالة رغبة الطرف الثاني بتجديد العقد لمدة أو مدد أخرى عليه إخطار الطرف الأول بذلك كتابيا قبل  ثلاثة (3)  أشهر من تاريخ إنتهاء العقد ولا يكون تجديد العقد نافذا إلا بعد موافقة كتابية من الطرف الأول .",
             "The Term of the Agreement is {(01) Year} Starting on {01 September 2022} (“Effective Date”) and expire on {31 August 2023} (“Expiry Date”) and no party has the right to terminate the Agreement before the Expiry date, unless otherwise provided by the Agreement. If the Second Party wishes to renew the Agreement for a similar period/s, he has to inform the First Party in writing three (3) months before the end of the Agreement. The renewal shall not be valid unless the First Party agrees in writing."),
            ("3",
             "إتفق الطرفان على أن قيمة إيجار {الفيلا }         ( العين المؤجرة) موضوع هذا العقد {12000 ر.ق ( اثنا عشر الف ريال قطري )} شهريا ويستحق الدفع في الأول من كل شهر بموجب شيكات يتم تسليمها للطرف الأول عند توقيع العقد",
             "The Parties agreed that the Rent value for the villa leased is QR. {12000} (Twelve Thousand Qatari Riyals Only) (“Rent”) to be paid at the beginning of each month by checks to be delivered to the First Party upon signing the Agreement."),
            ("4",
             "دون الإخلال بحقوق وامتيازات الطرف الأول بموجب هذا العقد او بموجب القانون، إذا لم يسدد الطرف الثاني أي من دفعات الإيجار بموجب هذا العقد في الأوقات أو خلال الفترة المحددة في هذا العقد، يلتزم المستأجر في تلك الحالة بأن يؤدي للمالك غرامة تأخير تعادل خمسة عشر بالمائة (١٥٪) من إجمالي الإيجار الشهري المستحق للطرف الاول عن كل اسبوع تأخير و ذلك بالإضافة إلى قيمة المبلغ المتأخر.",
             "Without prejudice to the rights and remedies of the First Party under this Agreement or under the law, if the Second Party fails to pay the Rent due to the First Party under the Agreement at the time or times or within the periods specified in the Agreement, then the tenant shall pay to the First Party the equivalent of Fifteen percent (15%) of the aggregate outstanding to the First Party per week, and that in addition to the overdue Rent amount."),
            ("5",
             "إتفق الطرفان على أن يقوم الطرف الثاني بتسديد رسوم إستهلاك وتأمين الماء والكهرباء والهاتف وكل ما شابه ، ولدى إنتهاء العقد وتركه للعين المؤجرة على الطرف الثاني أن يقوم بتسديد ما عليه من رسوم من قبل تلك الجهات أو غيرها.",
             "The Parties agreed that the Second Party shall pay all the charges for his consumption and the insurance deposit of water, electricity and phone etc. and upon the end of the Agreement, the Second Party shall pay all the due fees and charges of these services to any departments."),
            ("6",
             "اتفق الطرفان أنه للإبلاغ عن مشاكل الصيانة يقوم الطرف الثاني بارسال بريد إلكتروني الى العنوان main.atcm@gmail.com  أو التواصل عبر رقم الواتساب 33379725",
             "The Parties agreed that to report maintenance issue, Second Party shall send email to main.atcm@gmail.com or contact whatsapp number 33379725"),
            ("7",
             "يقر الطرف الثاني بأنه إستلم {الفيلا}(العين المؤجره)بعد أن عاينه ووجده بحالة جيده وصالح للغرض المعد لأجله.",
             "The Second Party acknowledges that he received the villa after he has inspected them thoroughly and find them fit for the purpose of the Lease."),
            ("8",
             "لا يحق للطرف الثاني أن يؤجر العين المؤجرة موضوع هذا العقد من الباطن أو التنازل عنها أو نقلها الى أحد غيره. كما يلتزم الطرف الثاني بإستخدام العين المؤجرة لعائلة فقط بدون إضافة أي جدران تقسيم  أو  تعديل البناء. كما يحق للطرف الأول القيام بزيارة ودخول العين المؤجرة .",
             "The Second Party shall have no right to sublease, waive or transfer the premises to any other party. The Second Party shall use the leased premises for Family only Without installing any partition walls Or modifying the building. The First Party has also the right to conduct a visit and enter the leased premises."),
            ("9",
             "يلتزم الطرف الثاني بالمحافظة علي سلامة ونظافة العين المؤجرة ولا يجوز للطرف الثاني القيام بأي تعديلات أو إضافات في العين المؤجرة( على سبيل المثال لا الحصر كالهدم أو البناء ) إلا بعد الحصول علي موافقة خطية من الطرف الأول وموافقة الجهات المختصة، وفي حالة عدم الإلتزام بذلك يحق للطرف الأول فسخ هذا العقد وتؤول احقية التصرف في العين المؤجرة للطرف الاول وعلى الطرف الثاني إخلاء العين المؤجرة ودفع الإيجار المستحق عن المدة المتبقية من العقد أو أي مده أو مدد منه فورا دون الحاجه إلى أي إنذار أو كتاب خطي وعمل التعديلات اللازمة علي حساب الطرف الثاني.وعلى الطرف الأول صيانة المكيفات واصلاح واستبدال المعدات )غسالة صحون ، الثلاجة الخ) التي يقدمها الطرف الأول والمصابيح الكهربائية التي يقدمها الطرف الثاني.",
             "The Second Party shall maintain the Premises sound and clean. In addition, the Second Party may not make any amendments, or refurbishments to the leased premises including but not limited to (demolition, building, making partitions,) without a prior written notice from the First Party and the concerned parties. If the Second Party violated any of the foregoing, the First Party shall have the right to terminate the Agreement, and the Second Party shall evacuate the Premises and pay the due rent for the remaining period of the Agreement or any term or terms of the Agreement forthwith without further notices or written letters, and the First Party shall make the necessary amendments at the cost of the Second Party. The First Party has to do AC unit maintenance and repairs and replacement of equipment (Dishwasher, Fridge etc.) provided by the First Party and the light bulbs provided by the Second Party."),
            ("10",
             "وإذا أقام الطرف الثاني في العين المؤجرة بناء أو غرسا أو ديكورات أو غير ذلك من تحسينات بموافقة الطرف الاول  أو بدون موافقته فإنه يلتزم بإرجاع العين المؤجرة إلى حالتها التي كانت عليها عند إستلامه في حالة طلب الطرف الاول ذلك.",
             "If the Second Party made a building, planted, made decorations or improvements with or without the consent of the First Party, he shall return the premises to its original status if the owner requested so.")
            # Agreement Points (continued)
            , ("11",
               "عند انتهاء الاتفاقية ، لأي سبب من الأسباب ، يجب على الطرف الثاني إخلاء المبنى في تاريخ الاستحقاق وتسليمه إلى الطرف الأول بنفس الحالة التي تم تسليمها إليه دون إشعار آخر أو خطابات مكتوبة ، والدفع أي تعويض عن أي ضرر أو هلاك للمبنى ، وأي تكاليف عن الأضرار الناجمة ستخضع لموافقة الإدارة.",
               "Upon the end of the Agreement, for any reason, the Second Party shall evacuate the premises in the due date and hand it over to the First Party in the same status as it was handed over to them without further notice or written letters, and pay any compensation for any damage or perish to the Premises, any charges of damages due to wear and tear will be subject for management approval."),
            ("12",
             "يلتزم الطرف الثاني بالمحافظة على العين المؤجرة حسب ما هو معروف عرفا وقانونا طبقا للإلتزامات الخاصة بالمستأجر وبإصلاح ما يتلف بسبب سوء الإستعمال طيلة مدة العقد.",
             "The Second Party shall maintain the Premises in accordance with the customs and laws in the frame of the special obligations of the tenant, and maintain any damage resulted by abuse through the term of the Agreement."),
            ("13",
             "يتعهد الطرف الثاني بدفع تأمين {للفيلا} ( العين المؤجرة) مقداره إيجار شهر مـبلغ {12000 رق} { اثنا عشر الف ريال قطري } للطرف الأول ، ويحق للطرف الأول إستخدامه في حالة قيام الطرف الثاني بالإخلال بإلتزاماته المنصوص عليها في هذا العقد.",
             "The Second Party shall pay a deposit for Villa leased worth one month's rent QR. 12000 (Twelve Thousand Qatari Riyals Only) to the First Party. The First Party shall have the right to use the deposit if the Second Party violated any of the provisions of the Agreement."),
            ("14",
             "في حالة إخلال الطرف الثاني بأي بند من بنود هذا العقد يحق للطرف الأول أن يفسخ هذا العقد ويلتزم الطرف الثاني بإخلاء العين المؤجرة فورا دون الحاجة إلى إنذار أو كتاب خطي ،ويلتزم الطرف الثاني بدفع كامل الإيجار للمدة المتبقية من العقد أو الممدده له. وتؤول احقية التصرف بالعين المؤجرة فوراً للطرف الأول بصفته المالك الشرعي وتسقط جميع حقوق الطرف الثاني في المطالبة أو التعويض.",
             "If the Second Party violated any of the Agreement provisions, the First Party shall terminate the Agreement and the Second Party shall evacuate the premises forthwith without further notices or written letters, and the Second Party shall pay the Rent for the remaining period of the Agreement or any renewed period/s. In addition, the owner shall have the right to act as he deemed proper regarding the premises in his capacity as the legal owner, and the First Party shall have no right for claims or compensations."),
            ("15",
             "إذا رغب الطرف الثاني بترك العين المؤجرة قبل نهاية مدة العقد يلتزم الطرف الثاني بتسليم العين المؤجرة بالحالة التي إستلمها عليها ويلتزم بدفع إيجار كامل المدة المتبقية من العقد أو المدده له.",
             "If the Second Party wishes to leave the leased villa before the end of the Agreement, he shall hand over the premises in the same status as it was handed over to him and pay the full Rent for the remaining period of the Agreement or any renewed period/s."),
            ("16",
             "في حالة مغادرة المستأجر البلاد بصورة نهائية قبل انتهاء هذا العقد فان الطرف الثاني يكون ملزما باخطار الطرف الاول خطيا بذلك في مدة لا تقل عن شهر مع تقدمه صورة عن الغاء اقامته ليتم انهاء العقد بدون غرامة",
             "In the case of permanent departure from the country and vacating the leased property before the expiry of the agreement’s term, the second party shall be obliged to provide the first party with one (1) month written notice in advance, and submit to the first party the cancellation documents confirming the second party’s departure from the country, without penalty."),
            ("17",
             "لا يجوز للمستأجر الانخراط في أي تجارة أو نشاط غير قانوني ، و يجب عليه الحصول على موافقة خطية مسبقة من المؤجر قبل تنفيذ أي أنشطة تجارية أخرى داخل العين المؤجرة  وأي خرق لهذا الالتزام يمنح المؤجر الحق في إنهاء عقد الإيجار هذا دون أي اعتراض من المستأجر",
             "The Tenant shall not engage in any illegal trade or activity, and they must obtain the prior written consent of the lessor before carrying out any other business activities within the the premises and any breach of this obligation gives the lessor the right to terminate this lease agreement without any objection from the lessee."),
            ("18",
             "على المستأجر اتباع جميع قوانين دولة قطر فيما يتعلق بإستئجار هذه العين المؤجره",
             "Tenant should adhere to all Qatari law in regards to the rental of this property")
        ]

        for point in points:
            worksheet.write(row, 0, f"({point[0]})", text_format)
        worksheet.write(row, 1, point[1], text_format)
        worksheet.write(row, 6, point[2], text_format)
        row += 2  # Leave a blank row after each point

        # Concluding the Agreement
        worksheet.write(row, 0, "حرر هذا العقد من ثلاث نسخ أصلية ، نسختين للطرف الأول ونسخة للطرف الثاني",
                        text_center_format)
        worksheet.write(row, 6,
                        "This Agreement is concluded in three originals. Two copies for the First Party and one for the Second Party.",
                        text_center_format)
        row += 2  # Leave a blank row

        worksheet.write(row, 0, "الطرف الأول", text_center_format)
        worksheet.write(row, 6, "The First Party:", text_center_format)
        row += 1
        worksheet.write(row, 0, "السادة / التألق للمقاولات والصيانة ذ.م.م", text_center_format)
        worksheet.write(row, 6, "AL TAALUQ CONTRACTING AND MAINTENANCE", text_center_format)
        row += 2  # Leave a blank row

        worksheet.write(row, 0, "الطرف الثاني (المستأجر)", text_center_format)
        worksheet.write(row, 6, "The Second Party:", text_center_format)
        row += 1
        worksheet.write(row, 0, "{السيد}/ {arabic_name}", text_center_format)
        worksheet.write(row, 6, "{MR}. {Javier Borja Elizondo}", text_center_format)

        workbook.close()
        return xls_filename
