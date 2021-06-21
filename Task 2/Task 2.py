import csv
import numpy as np
import matplotlib.pyplot as plt

#users - количество пользователей, отправивших сообщения, messages - суммарное количество сообщений
class UsersMessages:
    def __init__(self, users=0, messages=0):
        self.users = users
        self.messages = messages
    def add_messages(self, new_messages):
        self.users += 1
        self.messages += new_messages
    def mean_messages(self):
        if (self.users > 0):
            return self.messages / self.users
        return 0

file_path = "dataset.csv"
file_obj = open(file_path, encoding="utf-8")
reader = csv.DictReader(file_obj, delimiter=',')

max_age = 122
max_friends = 10001
max_apps = 10
max_idwr = 104
max_idftwr = 46
max_icc = 52
max_calls = 59
max_comments_created = 665
max_timespent_s = 54411; #seconds
max_timespent_m = max_timespent_s // 60 + 1 #minutes

age = {"Кыргызстан1": np.array([0] * max_age), "Кыргызстан2": np.array([0] * max_age), "Латвия1": np.array([0] * max_age), "Латвия2": np.array([0] * max_age)}

messaging_PA = {"Кыргызстан": [UsersMessages() for _ in range(max_age)], "Латвия": [UsersMessages() for _ in range(max_age)]} #PA = per age. messaging_to_UC по возрасту
messaging_PF = {"Кыргызстан": [UsersMessages() for _ in range(max_friends)], "Латвия": [UsersMessages() for _ in range(max_friends)]} #PF = per friends
messaging_POA = {"Кыргызстан": [UsersMessages() for _ in range(max_apps)], "Латвия": [UsersMessages() for _ in range(max_apps)]} #POA = per other apps
messaging_PIDWR = {"Кыргызстан": [UsersMessages() for _ in range(max_idwr)], "Латвия": [UsersMessages() for _ in range(max_idwr)]} #PIDWR = per inited_direct_with_reply
messaging_PIDFTWR = {"Кыргызстан": [UsersMessages() for _ in range(max_idftwr)], "Латвия": [UsersMessages() for _ in range(max_idftwr)]} #PIDFTWR = per inited_direct_first_time_with_reply
messaging_PICC = {"Кыргызстан": [UsersMessages() for _ in range(max_icc)], "Латвия": [UsersMessages() for _ in range(max_icc)]} #PICC = per inited_chat_conversations
messaging_PC = {"Кыргызстан": [UsersMessages() for _ in range(max_calls)], "Латвия": [UsersMessages() for _ in range(max_calls)]} #PC = per calls
messaging_PCC = {"Кыргызстан": [UsersMessages() for _ in range(max_comments_created)], "Латвия": [UsersMessages() for _ in range(max_comments_created)]} #PCC = per comments created
messaging_PT = {"Кыргызстан": [UsersMessages() for _ in range(max_timespent_m)], "Латвия": [UsersMessages() for _ in range(max_timespent_m)]} #PT = per time spent

for line in reader:
    user_botscore = float(line["user_botscore"])

    #данные для оценки состава стран
    auditory_country_id = line["auditory_country_id"]
    user_sex = line["user_sex"]
    country_sex = auditory_country_id + user_sex
    user_age = int(line["user_age"])

    #критерии активности
    user_friends = int(line["user_friends"])
    other_apps_total = int(line["has_app_facebook"]) + int(line["has_app_facebook_messenger"]) + int(line["has_app_whatsapp"]) + int(line["has_app_telegram"]) + int(line["has_app_instagram"]) + int(line["has_app_skype"]) + int(line["has_app_viber"]) + int(line["has_app_tiktok"]) + int(line["has_app_ok"])
    messaging_inited_direct_with_reply = int(line["messaging_inited_direct_with_reply"])
    messaging_inited_direct_first_time_with_reply = int(line["messaging_inited_direct_first_time_with_reply"])
    messaging_inited_chat_conversations = int(line["messaging_inited_chat_conversations"])
    calls = int(line["calls"])
    comments_created = int(line["comments_created"])
    timespent_im = int(line["timespent_im"]) // 60

    #количество сообщений
    messaging_total = int(line["messaging_total"])
    messaging_total_to_users = int(line["messaging_total_to_users"])
    messaging_total_to_chats = int(line["messaging_total_to_chats"])
    messaging_to_UC = messaging_total_to_users + messaging_total_to_chats

    if (user_botscore < 0.3):
        age[country_sex][user_age] += 1
        if (messaging_to_UC > 0):
            messaging_PA[auditory_country_id][user_age].add_messages(messaging_to_UC)
            messaging_PF[auditory_country_id][user_friends].add_messages(messaging_to_UC)
            messaging_POA[auditory_country_id][other_apps_total].add_messages(messaging_to_UC)
            messaging_PIDWR[auditory_country_id][messaging_inited_direct_with_reply].add_messages(messaging_to_UC)
            messaging_PIDFTWR[auditory_country_id][messaging_inited_direct_first_time_with_reply].add_messages(messaging_to_UC)
            messaging_PICC[auditory_country_id][messaging_inited_chat_conversations].add_messages(messaging_to_UC)
            messaging_PC[auditory_country_id][calls].add_messages(messaging_to_UC)
            messaging_PCC[auditory_country_id][comments_created].add_messages(messaging_to_UC)
            messaging_PT[auditory_country_id][timespent_im].add_messages(messaging_to_UC)

age_total_k = sum(age["Кыргызстан1"]) + sum(age["Кыргызстан2"])
age_total_l = sum(age["Латвия1"]) + sum(age["Латвия2"])
print("age_total_k1 =", sum(age["Кыргызстан1"]))
print("age_total_k2 =", sum(age["Кыргызстан2"]))
print("age_total_k =", age_total_k)
print("age_total_l1 =", sum(age["Латвия1"]))
print("age_total_l2 =", sum(age["Латвия2"]))
print("age_total_l =", age_total_l)

fig, ax = plt.subplots(4, 1)
ax[0].bar(np.arange(0, max_age), age["Кыргызстан1"] / age_total_k * 100, label="Кыргызстан Ж")
ax[1].bar(np.arange(0, max_age), age["Кыргызстан2"] / age_total_k * 100, label="Кыргызстан М")
ax[2].bar(np.arange(0, max_age), age["Латвия1"] / age_total_l * 100, label = "Латвия Ж")
ax[3].bar(np.arange(0, max_age), age["Латвия2"] / age_total_l * 100, label = "Латвия М")
ax[3].set_xlabel("Возраст")
ax[3].set_ylabel("Доля пользователей (%) в стране")
ax[0].legend(); ax[1].legend(); ax[2].legend(); ax[3].legend()

fig2, ax2 = plt.subplots(2, 1)
ax2[0].bar(np.arange(0, max_age), [um.mean_messages() for um in messaging_PA["Кыргызстан"]])
ax2[0].set_title("Кыргызстан")
ax2[1].bar(np.arange(0, max_age), [um.mean_messages() for um in messaging_PA["Латвия"]])
ax2[1].set_title("Латвия")
ax2[1].set_xlabel("Возраст")
ax2[1].set_ylabel("Среднее количество сообщений")

fig3, ax3 = plt.subplots(2, 1)
ax3[0].bar(np.arange(0, max_friends), [um.mean_messages() for um in messaging_PF["Кыргызстан"]])
ax3[0].set_title("Кыргызстан")
ax3[1].bar(np.arange(0, max_friends), [um.mean_messages() for um in messaging_PF["Латвия"]])
ax3[1].set_title("Латвия")
ax3[1].set_xlabel("Количество друзей")
ax3[1].set_ylabel("Среднее количество сообщений")

fig4, ax4 = plt.subplots(2, 1)
ax4[0].bar(np.arange(0, max_apps), [um.mean_messages() for um in messaging_POA["Кыргызстан"]])
ax4[0].set_title("Кыргызстан")
ax4[1].bar(np.arange(0, max_apps), [um.mean_messages() for um in messaging_POA["Латвия"]])
ax4[1].set_title("Латвия")
ax4[1].set_xlabel("Количество других приложений")
ax4[1].set_ylabel("Среднее количество сообщений")

fig5, ax5 = plt.subplots(2, 1)
ax5[0].bar(np.arange(0, max_idwr), [um.mean_messages() for um in messaging_PIDWR["Кыргызстан"]])
ax5[0].set_title("Кыргызстан")
ax5[1].bar(np.arange(0, max_idwr), [um.mean_messages() for um in messaging_PIDWR["Латвия"]])
ax5[1].set_title("Латвия")
ax5[1].set_xlabel("Количество инициированных личных бесед с ответом")
ax5[1].set_ylabel("Среднее количество сообщений")

fig6, ax6 = plt.subplots(2, 1)
ax6[0].bar(np.arange(0, max_idftwr), [um.mean_messages() for um in messaging_PIDFTWR["Кыргызстан"]])
ax6[0].set_title("Кыргызстан")
ax6[1].bar(np.arange(0, max_idftwr), [um.mean_messages() for um in messaging_PIDFTWR["Латвия"]])
ax6[1].set_title("Латвия")
ax6[1].set_xlabel("Количество впервые инициированных личных бесед с ответом")
ax6[1].set_ylabel("Среднее количество сообщений")

fig7, ax7 = plt.subplots(2, 1)
ax7[0].bar(np.arange(0, max_icc), [um.mean_messages() for um in messaging_PICC["Кыргызстан"]])
ax7[0].set_title("Кыргызстан")
ax7[1].bar(np.arange(0, max_icc), [um.mean_messages() for um in messaging_PICC["Латвия"]])
ax7[1].set_title("Латвия")
ax7[1].set_xlabel("Количество инициированных чатов")
ax7[1].set_ylabel("Среднее количество сообщений")

fig8, ax8 = plt.subplots(2, 1)
ax8[0].bar(np.arange(0, max_calls), [um.mean_messages() for um in messaging_PC["Кыргызстан"]])
ax8[0].set_title("Кыргызстан")
ax8[1].bar(np.arange(0, max_calls), [um.mean_messages() for um in messaging_PC["Латвия"]])
ax8[1].set_title("Латвия")
ax8[1].set_xlabel("Количество инициированных звонков")
ax8[1].set_ylabel("Среднее количество сообщений")

fig9, ax9 = plt.subplots(2, 1)
ax9[0].bar(np.arange(0, max_comments_created), [um.mean_messages() for um in messaging_PCC["Кыргызстан"]])
ax9[0].set_title("Кыргызстан")
ax9[1].bar(np.arange(0, max_comments_created), [um.mean_messages() for um in messaging_PCC["Латвия"]])
ax9[1].set_title("Латвия")
ax9[1].set_xlabel("Количество написанных комментариев")
ax9[1].set_ylabel("Среднее количество сообщений")

fig10, ax10 = plt.subplots(2, 1)
ax10[0].bar(np.arange(0, max_timespent_m), [um.mean_messages() for um in messaging_PT["Кыргызстан"]])
ax10[0].set_title("Кыргызстан")
ax10[1].bar(np.arange(0, max_timespent_m), [um.mean_messages() for um in messaging_PT["Латвия"]])
ax10[1].set_title("Латвия")
ax10[1].set_xlabel("Проведенное время в 'Мессенджере' (мин)")
ax10[1].set_ylabel("Среднее количество сообщений")

plt.show()

file_obj.close()