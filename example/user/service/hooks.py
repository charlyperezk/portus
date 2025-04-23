from example.user.service.methods import create_life_cycle, update_life_cycle, delete_life_cycle

user_hooks = {
    'create': create_life_cycle,
    'update': update_life_cycle,
    'delete': delete_life_cycle
}