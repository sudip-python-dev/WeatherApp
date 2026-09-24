import pickle

api_key = input("Enter your OpenWeatherMap API Key: ").strip()

with open('.key.db', 'wb') as f:
    pickle.dump({'key': api_key}, f)

print("API Key saved successfully in .key.db!")

