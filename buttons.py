

if __name__ == "__main__":
    import platform
    Color = platform.Color.instance()
    Game(color=Color).loop()
