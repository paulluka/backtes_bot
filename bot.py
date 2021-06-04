def behaviour(df, i0, fenetre):

	m = i0
	
	assets = i0/df["Close"].iloc[-1*fenetre]

	close = df["Close"].tolist()

	m_a_5d = df["m_a_5d"].tolist()
	m_a_9d = df["m_a_9d"].tolist()
	
	sig = []
	for i in range(len(m_a_5d)):
		if m_a_9d[i] >= m_a_5d[i]:
			sig.append(1)
		else:
			sig.append(-1)

	k = sig[0]
	for i in range(len(sig)):
		if sig[i] == k:
			sig[i] = 0
		else:
			k = sig[i]

	recette = []

	for i in range(len(sig)):
		if sig[i] == 1 and m != 0:
			assets = m/close[i]
			m = 0
			recette.append(assets*close[i])

		elif sig[i] == -1 and assets != 0:
			m = assets*close[i]
			assets = 0
			recette.append(m)

		else:
			recette.append(m + assets*close[i])





	df.insert(8, "signal", sig, allow_duplicates=False)
	df.insert(8, "recette", recette, allow_duplicates=False)

	


	return df