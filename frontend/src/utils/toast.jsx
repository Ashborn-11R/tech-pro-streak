import toast from 'react-hot-toast';

const base = {
  color: '#fff',
  padding: '16px 24px',
  borderRadius: '12px',
  fontSize: '0.95rem',
  fontWeight: '600',
  backdropFilter: 'blur(10px)',
};

export const showSuccess = (message, options = {}) =>
  toast.success(message, {
    duration: 3000,
    position: 'top-center',
    style: { ...base, background: 'rgba(16, 185, 129, 0.95)' },
    ...options,
  });

export const showError = (message, options = {}) =>
  toast.error(message, {
    duration: 4000,
    position: 'top-center',
    style: { ...base, background: 'rgba(239, 68, 68, 0.95)' },
    ...options,
  });

export const showInfo = (message, options = {}) =>
  toast(message, {
    duration: 3000,
    position: 'top-center',
    icon: 'ℹ️',
    style: { ...base, background: 'rgba(59, 130, 246, 0.95)' },
    ...options,
  });

export const showWithAction = (message, actionLabel, onAction, options = {}) =>
  toast(
    (t) => (
      <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
        <span>{message}</span>
        <button
          onClick={() => {
            onAction();
            toast.dismiss(t.id);
          }}
          style={{
            background: 'rgba(255,255,255,0.2)',
            border: '1px solid rgba(255,255,255,0.3)',
            color: '#fff',
            padding: '6px 14px',
            borderRadius: '8px',
            cursor: 'pointer',
            fontWeight: '700',
          }}
        >
          {actionLabel}
        </button>
      </div>
    ),
    {
      duration: 5000,
      position: 'bottom-center',
      style: { ...base, background: 'rgba(124, 58, 237, 0.95)', maxWidth: '500px' },
      ...options,
    }
  );