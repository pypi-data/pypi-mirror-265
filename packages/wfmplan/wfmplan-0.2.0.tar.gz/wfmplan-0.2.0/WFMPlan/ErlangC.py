import pandas as pd
from math import factorial, e, ceil

class ErlangC:
    def __init__(self, data, target_method='sla'):
        self.data = data
        self.target = target_method
      
    def prob_waiting(self, traffic_intensity, num_agents):
        x = ((traffic_intensity ** num_agents) / factorial(round(num_agents))) * num_agents / (num_agents - traffic_intensity)
        y = 1

        for i in range(round(num_agents)):
            y += (traffic_intensity ** i) / factorial(i)

        return x / (y + x)

    def compute_sla(self, pw, traffic_intensity, num_agents, targ_ans_time, aht):
        return 1 - (pw * (e ** -((num_agents - traffic_intensity) * (targ_ans_time / aht))))

    def get_erlang_c(self, row):
        volume = row['volume']
        traffic_intensity = row['volume'] * (row['target_aht']/60)/(row['interval_size'])
        target_answer_time = row['target_service_time']
        aht_seconds = row['target_aht']
        target_sla = row['target_sla']
        shrinkage = row['target_shrink']

        raw_agent = 1
        n = round(traffic_intensity + raw_agent)

        pw = self.prob_waiting(traffic_intensity, n)

        act_sla = self.compute_sla(pw, traffic_intensity, n, target_answer_time, aht_seconds)

        while act_sla < target_sla:
            raw_agent += 1
            n = round(traffic_intensity + raw_agent)
            pw = self.prob_waiting(traffic_intensity, n)
            act_sla = self.compute_sla(pw, traffic_intensity, n, target_answer_time, aht_seconds)

        average_speed_of_answer = (pw * aht_seconds) / (n - traffic_intensity)

        percent_calls_answered_immediately = (1 - pw) * 100

        maximum_occupancy = (traffic_intensity / n) * 100

        n_shrinkage = n / (1 - shrinkage)

        return {
            'pred_AgentRequired': int(n),
            'pred_AgentRequiredWithShrink': ceil(n_shrinkage),
            'pred_ASA': round(average_speed_of_answer, 1),
            'pred_Occupancy': round(maximum_occupancy, 2),
            'pred_SLA': round((act_sla * 100), 2)
        }

    def predict(self):
        df = pd.DataFrame(self.data)
        df['ds'] = pd.to_datetime(df['ds'])
       
        if (df['volume'] <= 0).any():
            raise ValueError("Transactions can't be smaller or equal to 0")
        if (df['target_aht'] <= 0).any():
            raise ValueError("AHT can't be smaller or equal to 0")
        if (df['interval_size'] <= 0).any():
            raise ValueError("Interval size can't be smaller or equal to 0")
        if (df['target_sla'] <= 0).any() or (df['target_sla'] > 1).any():
            raise ValueError("target_sla should be between 0% to 100%")
        if (df['target_service_time'] <= 0).any():
            raise ValueError("Service time target can't be smaller or equal to 0")
        if (df['target_asa'] <= 0).any():
            raise ValueError("ASA target can't be smaller or equal to 0")
        if (df['target_max_occupancy'] <= 0).any() or (df['target_max_occupancy'] > 1).any():
            raise ValueError("target_max_occupancy should be between 0% to 100%")
        if (df['target_shrink'] <= 0).any():
            raise ValueError("Shrinkage target can't be smaller or equal to 0")
         
        self.n_transactions = df['volume']
        self.aht = df['target_aht']
        self.interval = df['interval_size']
        self.asa = df['target_asa']
        self.shrinkage = df['target_shrink']
           
        result = df.apply(self.get_erlang_c, axis=1)
        result_df = pd.json_normalize(result)
        return pd.concat([df, result_df], axis=1)