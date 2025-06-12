import pandas as pd
import numpy as np

import pulp

import argparse


PREF_CITY: list[tuple[str, str]] = [
        ("北海道", "札幌市"),
        ("青森県", "青森市"),
        ("岩手県", "盛岡市"),
        ("宮城県", "仙台市"),
        ("秋田県", "秋田市"),
        ("山形県", "山形市"),
        ("福島県", "福島市"),
        ("茨城県", "水戸市"),
        ("栃木県", "宇都宮市"),
        ("群馬県", "前橋市"),
        ("埼玉県", "さいたま市"),
        ("千葉県", "千葉市"),
        ("東京都", None),
        ("神奈川県", "横浜市"),
        ("新潟県", "新潟市"),
        ("富山県", "富山市"),
        ("石川県", "金沢市"),
        ("福井県", "福井市"),
        ("山梨県", "甲府市"),
        ("長野県", "長野市"),
        ("岐阜県", "岐阜市"),
        ("静岡県", "静岡市"),
        ("愛知県", "名古屋市"),
        ("三重県", "津市"),
        ("滋賀県", "大津市"),
        ("京都府", "京都市"),
        ("大阪府", "大阪市"),
        ("兵庫県", "神戸市"),
        ("奈良県", "奈良市"),
        ("和歌山県", "和歌山市"),
        ("鳥取県", "鳥取市"),
        ("島根県", "松江市"),
        ("岡山県", "岡山市"),
        ("広島県", "広島市"),
        ("山口県", "山口市"),
        ("徳島県", "徳島市"),
        ("香川県", "高松市"),
        ("愛媛県", "松山市"),
        ("高知県", "高知市"),
        ("福岡県", "福岡市"),
        ("佐賀県", "佐賀市"),
        ("長崎県", "長崎市"),
        ("熊本県", "熊本市"),
        ("大分県", "大分市"),
        ("宮崎県", "宮崎市"),
        ("鹿児島県", "鹿児島市"),
        ("沖縄県", "那覇市")
        ]


def load_data(args: argparse.Namespace = None) -> dict[str, pd.DataFrame]:
    if args:
        assert args.population is not None
        assert args.consumption is not None
        assert args.production is not None
        assert args.distance is not None

        return {
                "population": pd.read_excel(args.population),
                "consumption": pd.read_excel(args.consumption, 1),
                "production": pd.read_excel(args.production),
                "distance": pd.read_csv(args.distance)
                }
    return {
            "population": pd.read_excel("24ntjin.xlsx"),
            "consumption": pd.read_excel("a401.xlsx", 1),
            "production": pd.read_excel("f005-05-063.xlsx"),
            "distance": pd.read_csv("prefecture_capital_distances.csv"),
            # "legend": pd.read_excel("kouh2020.xlsx")
            }


def get_population(data: pd.DataFrame) -> dict[str, int]:
    # Data starts from 4.
    population: dict[str, int] = {"東京都": 0}  # Need initialization
    for i in range(4, data.shape[0]):
        pref: str = data.iat[i, 1]
        city: str = data.iat[i, 2]
        if (pref, city) in PREF_CITY:
            try:
                population[data.iat[i, 1]] = int(data.iat[i, 6])
            except ValueError:
                population[data.iat[i, 1]] = 0
        if (pref == "東京都") and ((type(city) is str) and city.endswith("区")):
            try:
                population[data.iat[i, 1]] += int(data.iat[i, 6])
            except ValueError:
                pass
    return population


def get_population_j(data: pd.DataFrame) -> dict[str, int]:
    population: dict[str, int] = {}
    for i in range(6, data.shape[0]):
        pref: str = data.iat[i, 1]
        for p, _ in PREF_CITY:
            if p == pref:
                try:
                    population[p] = int(data.iat[i, 5])
                except ValueError:
                    population[p] = 0
    return population


def get_consumption(data: pd.DataFrame, name: str) -> dict[str, float]:
    consumption: dict[str, int] = {}
    name_idx: int = None
    for i in range(data.shape[0]):
        if data.iat[i, 11] == name:
            name_idx = i
    if name_idx is None:
        print("Error at get consumption")
        exit(1)

    for pref, city in PREF_CITY:
        if pref == "東京都":
            city = "東京都区部"
        tgt: str = f"{city}・購入数量"
        for i in range(14, data.shape[1]):
            label: str = str(data.iat[7, i])
            label = label[label.find(' ') + 1:]
            # if str(data.iat[7, i]).endswith(tgt):
            if label == tgt:
                try:
                    consumption[pref] = float(data.iat[name_idx, i])
                except ValueError:
                    consumption[pref] = 0.0
    return consumption


def get_production(data: pd.DataFrame) -> dict[str, float]:
    production: dict[str, int] = {}
    # Data starts from 16
    for pref, _ in PREF_CITY:
        _pref: str = pref
        if pref != "北海道":
            _pref = _pref[:-1]
        for i in range(16, data.shape[0]):
            # if pref.find(str(data.iat[i, 0])) != -1:
            if data.iat[i, 0] == _pref:
                try:
                    production[pref] = int(data.iat[i, 5])
                except ValueError:
                    production[pref] = 0
    return production


def get_unit_cost(data: pd.DataFrame, name: str) -> dict[str, float]:
    unit_cost: dict[str, int] = {}
    name_idx: int = None
    for i in range(data.shape[0]):
        if data.iat[i, 11] == name:
            name_idx = i
    if name_idx is None:
        print("Error at get consumption")
        exit(1)

    for pref, city in PREF_CITY:
        if pref == "東京都":
            city = "東京都区部"
        tgt: str = f"{city}・平均価格"
        for i in range(14, data.shape[1]):
            label: str = str(data.iat[7, i])
            label = label[label.find(' ') + 1:]
            # if str(data.iat[7, i]).endswith(tgt):
            if label == tgt:
                try:
                    unit_cost[pref] = float(data.iat[name_idx, i])
                except ValueError:
                    unit_cost[pref] = 0.0
    return unit_cost


def get_distance(data: pd.DataFrame) -> dict[tuple[str, str], float]:
    distance: dict[tuple[str, str], float] = {}

    for pref0, city0 in PREF_CITY:
        if pref0 == "東京都":
            city0 = "東京都区部"
        for pref1, city1 in PREF_CITY:
            if pref1 == "東京都":
                city1 = "東京都区部"
            city: tuple[str, str] = (city0, city1)
            cidx: int = None
            for k in range(data.shape[1]):
                if data.columns[k] == city[1]:
                    cidx = k
            assert cidx is not None

            for k in range(data.shape[0]):
                if data.iat[k, 0] == city[0]:
                    distance[(pref0, pref1)] = float(data.iat[k, cidx])
    return distance


def get_transportation_cost_s(data: pd.DataFrame) -> dict[float, float]:
    raise NotImplementedError()


def get_transportation_cost_m(
        data: pd.DataFrame) -> dict[tuple[float, float], float]:
    cost: dict[tuple[float, float], float] = {}
    for i, l in enumerate(data.columns[1:]):
        lf: float = float(l)
        for k in range(data.shape[0]):
            dist: float = float(data.iat[k, 0])
            c: float = float(data.iat[k, i + 1])
            cost[(lf, dist)] = c
    return cost


def get_transportation_cost(
        data: pd.DataFrame, simple=False
        ) -> dict[float, float] | dict[tuple[float, float], float]:
    if len(data.columns) == 2:
        return get_transportation_cost_s(data)
    if len(data.columns) > 2:
        d: dict[tuple[float, float], float] = get_transportation_cost_m(data)
        if not simple:
            return d

        d_s: dict[float, float] = {}
        t: set = set()
        for k, v in d.items():
            t |= set([k[0]])
            if not k[1] in d_s.keys():
                d_s[k[1]] = 0
            d_s[k[1]] += v / k[0]
        for k in d_s.keys():
            d_s[k] /= len(t)

        for k, v in d_s.items():
            print(k, v)
        return d_s
    raise NotImplementedError()


def calculate_consumption(
        consumption: dict[str, int], population: dict[str, int], unit: float
        ) -> dict[str, float]:
    cp: dict[str, float] = {}
    for k in consumption.keys():
        cp[k] = consumption[k] * population[k] / float(unit)
    return cp


def calculate_unit_cost(unit_cost: dict[str, float], unit: float
                        ) -> dict[str, int]:
    uc: dict[str, float] = {}
    for k in unit_cost.keys():
        uc[k] = unit_cost[k] * float(unit)
    return uc


def profit_maximization(
        production: dict[str, float], consumption: dict[str, float],
        unit_cost: dict[str, float], distance: dict[tuple[str, str], float],
        transportation_cost: dict[float, float]) -> pulp.LpVariable:
    problem: pulp.LpProblem = pulp.LpProblem("Profit ;)", pulp.LpMaximize)
    shipment: pulp.LpVariable = pulp.LpVariable.dicts(
            "x", list(distance.keys()),
            lowBound=0, cat="Continuous")

    tcost_keys: list[float] = list(sorted(list(transportation_cost.keys())))
    dist_transport_cost: dict[tuple[str, str], float] = {}
    for k, v in distance.items():
        if v == 0:
            dist_transport_cost[k] = 1
            continue
        for tk in reversed(tcost_keys):
            while (v - tk) > 0:
                v -= tk
                if k in dist_transport_cost.keys():
                    dist_transport_cost[k] += tk
                else:
                    dist_transport_cost[k] = tk

    problem += pulp.lpSum(
            (unit_cost[k[1]] * shipment[k]
             ) - shipment[k] * dist_transport_cost[k] for k in distance.keys())

    # Condition 1
    for p, _ in PREF_CITY:
        problem += pulp.lpSum(
                shipment[(p, p2)] for p2, _ in PREF_CITY) <= production[p]
    # Condition 2
    for p, _ in PREF_CITY:
        problem += pulp.lpSum(
                shipment[(p2, p)] for p2, _ in PREF_CITY) <= consumption[p]

    status = problem.solve()
    if status != pulp.LpStatusOptimal:
        print(f"Optimal value didn't find: {status}")
    return shipment


def profit_maximization_detailed(
        production: dict[str, float], consumption: dict[str, float],
        unit_cost: dict[str, float], distance: dict[tuple[str, str], float],
        transportation_cost: dict[float, dict[float, float]]
        ) -> pulp.LpVariable:
    raise NotImplementedError()


def main(args: argparse.Namespace):
    data: dict[str, pd.DataFrame] = {}

    try:
        data = load_data(args)
    except Exception as e:
        print(e)
        exit(1)

    # pop: dict[str, int] = get_population(data["population"])
    pop: dict[str, int] = {}
    if args.population_mode == "japanese":
        pop = get_population_j(data["population"])
    if args.population_mode == "total":
        pop = get_population(data["population"])
    con: dict[str, float] = get_consumption(data["consumption"], args.item)
    uni: dict[str, float] = get_unit_cost(data["consumption"], args.item)
    pro: dict[str, float] = get_production(data["production"])
    dis: dict[tuple[str, str], float] = get_distance(data["distance"])
    assert len(pop.keys()) == 47
    assert len(con.keys()) == 47
    assert len(uni.keys()) == 47
    assert len(pro.keys()) == 47
    assert (len(dis.keys()) == 47**2)
    assert pop.keys() == con.keys()
    assert con.keys() == uni.keys()
    assert uni.keys() == pro.keys()

    if args.dataset:
        with open("households.csv", "w", encoding="utf-8") as f:
            print("都市名,世帯数", file=f)
            for k, v in pop.items():
                print(f"{k},{v}", file=f)

        with open("consumption.csv", "w", encoding="utf-8") as f:
            print("県名,購入数量", file=f)
            for k, v in con.items():
                print(f"{k},{v}", file=f)

        with open("production.csv", "w", encoding="utf-8") as f:
            print("県名,生産量", file=f)
            for k, v in pro.items():
                print(f"{k},{v}", file=f)

    con = calculate_consumption(con, pop, args.unit)
    uni = calculate_unit_cost(uni, args.unit_cost)
    assert pop.keys() == con.keys()
    assert pop.keys() == uni.keys()

    if args.profit:
        print("Profit mode")
        tra: dict[float, float] = get_transportation_cost(
                pd.read_csv(args.transportation), simple=True)
        shipment = profit_maximization(pro, con, uni, dis, tra)
    else:
        print("Shipment mode")
        problem: pulp.LpProblem = pulp.LpProblem(":3", pulp.LpMinimize)
        shipment: pulp.LpVariable = pulp.LpVariable.dicts(
                "x", list(dis.keys()), lowBound=0, cat="Continuous")

        problem += pulp.lpSum(shipment[k] * dis[k] for k in dis.keys())

        # Condition 1
        for p, _ in PREF_CITY:
            problem += pulp.lpSum(
                    shipment[(p, p2)] for p2, _ in PREF_CITY) <= pro[p]
        # Condition 2
        for p, _ in PREF_CITY:
            problem += pulp.lpSum(
                    shipment[(p2, p)] for p2, _ in PREF_CITY) == con[p]

        status = problem.solve()
        if status != pulp.LpStatusOptimal:
            print(f"Optimal value didn't find: {status}")

    shipment_mat: np.ndarray = np.zeros((len(PREF_CITY), len(PREF_CITY)))
    for iidx, (i, _) in enumerate(PREF_CITY):
        for jidx, (j, _) in enumerate(PREF_CITY):
            shipment_mat[iidx][jidx] = pulp.value(shipment[(i, j)])
            # assert shipment_mat[iidx][jidx] >= 0

    city_names: list[str] = []
    for p, c in PREF_CITY:
        if p == "東京都":
            c = "東京都区部"
        city_names.append(c)
    shipment_data: pd.DataFrame = pd.DataFrame(
            shipment_mat, index=city_names, columns=city_names)
    print(shipment_data)
    if args.shipment:
        shipment_data.to_csv(args.shipment, encoding="utf-8")


if __name__ == "__main__":
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument("--population", help="Dataset of population")
    parser.add_argument(
            "--population-mode", default="total",
            choices=["japanese", "total"], help="Population dataset type")
    parser.add_argument("--consumption", help="Dataset of consumption")
    parser.add_argument("--production", help="Dataset of production")
    parser.add_argument(
            "--distance", default="prefecture_capital_distances.csv",
            help="Dataset of distance")
    parser.add_argument("--transportation", default="transportation_cost.csv",
                        help="Dataset of transportation cost")
    parser.add_argument(
            "--item", help="Item name to search data from consumption")
    parser.add_argument(
            "--unit", default=1000000, type=float,
            help="Unit to calculate consumption (ex: 1000000 for tomato)")
    parser.add_argument(
            "--unit-cost", default=10000, type=float,
            help="Unit to calculate average cost (ex. 10000 for tomato)")
    parser.add_argument("--dataset", action="store_true",
                        help="Produce dataset compatible for lp_full.py")
    parser.add_argument("--shipment", help="File path to save result data")
    parser.add_argument(
            "--profit", action="store_true",
            help="Caclulate profix maximization")
    main(parser.parse_args())
