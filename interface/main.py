
def main():
    import src
    app = src.App()
    app.app.run(use_reloader=True)


if __name__ == '__main__':
    main()