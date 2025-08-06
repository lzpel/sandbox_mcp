import dreamerv3
import gym
import os

# ==== 設定 ====
ENV_NAME = "ALE/Breakout-v5"   # Atariゲームの選択
RUN_DIR = "./logdir/breakout_demo"

# ==== 環境の用意 ====
env = gym.make(ENV_NAME, render_mode='rgb_array')
act_space = env.action_space.n
obs_space = env.observation_space

# ==== DreamerV3の設定 ====
config = dreamerv3.defaults.update({
    'logdir': RUN_DIR,
    'run.train_ratio': 64,
    'run.steps': 2e5,        # 学習ステップ（デモでは短め）
    'env.task': ENV_NAME,
    'env.atari_grayscale': True,
    'env.atari_action_repeat': 4,
    'env.atari_sticky_actions': True,
    'env.atari_noops': 30,
    'run.eval_every': 5e3,
})

# ==== エージェントの作成 ====
agent = dreamerv3.Agent(obs_space, act_space, config)

# ==== 簡易ループ ====
steps = 0
episodes = 0
while steps < config['run.steps']:
    obs, _ = env.reset()
    agent_episode = agent.policy.reset()
    done = False
    total_reward = 0

    while not done:
        action = agent.policy(obs)
        next_obs, reward, terminated, truncated, info = env.step(action)
        done = terminated or truncated
        agent.policy.feed(obs, action, reward, next_obs, done)
        obs = next_obs
        total_reward += reward
        steps += 1

        if steps % 1000 == 0:
            print(f"Steps: {steps}, Episodes: {episodes}, Reward: {total_reward}")

    episodes += 1

print("Training finished. Now evaluating the learned policy...")

# ==== 評価ループ（プレイ観察）====
obs, _ = env.reset()
done = False
while not done:
    action = agent.policy(obs, training=False)
    obs, reward, terminated, truncated, _ = env.step(action)
    done = terminated or truncated
    env.render()  # 画面に表示