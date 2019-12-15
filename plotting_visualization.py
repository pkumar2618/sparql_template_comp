import pandas as pd
import matplotlib.pyplot as plt

with open("stats_qaldCombined_vs_LCQUAD2.csv", 'r') as file_handle:
    raw_df = pd.read_csv(file_handle)
    # raw_df.plot.pie(y="question_type")
    unique_qType_dict = {}
    for q_type in raw_df["question_type"]:
        if q_type not in unique_qType_dict.keys():
            unique_qType_dict[q_type] = 1
        elif q_type in unique_qType_dict.keys():
            unique_qType_dict[q_type] += 1

    qType_stats_df = pd.DataFrame.from_dict(unique_qType_dict, orient='index')
    qType_stats_df.columns = ['Question Type']
    qType_stats_df.plot.pie(y='Question Type', autopct = '%.2f')
    plt.title('Type of questions in QALD-Combined')

    # plt.savefig('qaldComb_piepalot.pdf', bbox_inches='tight')
    plt.savefig('qaldComb_piepalot.png', bbox_inches='tight')
    # qType_stats_df.plot()
    # plt.show()