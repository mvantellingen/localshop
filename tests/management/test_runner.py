from localshop.runner import main


def test_main(monkeypatch):
    from django.core import management

    def mock_exec(args):
        return

    monkeypatch.setattr(management, 'execute_from_command_line', mock_exec)

    main()
