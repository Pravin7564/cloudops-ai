from backend.services.log_analyzer import LogAnalyzer


def main():
    analyzer = LogAnalyzer()

    sample_log = """
Warning BackOff Back-off restarting failed container
CrashLoopBackOff
"""

    result = analyzer.analyze(sample_log)

    print(result)


if __name__ == "__main__":
    main()