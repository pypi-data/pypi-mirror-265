from nezu.nezu import Nezu

def test_instances():
    n1 = Nezu('n1')
    n1(3)
    n2 = Nezu('n2')
    n2(6,1)
    assert dict(n1) == {'id': 'n1', 'seek': 3, 'color': False}
    assert dict(n2) == {'id': 'n2', 'seek': 6, 'color': True}